from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import TeacherProfile, Skill, TeacherSkill, Review, Student
from .forms import TeacherProfileForm, TeacherSkillForm, ReviewForm, TeacherSearchForm, StudentUpdateForm, StudentProfileUpdateForm
from users.models import User
from users.forms import UserUpdateForm
from .filters import TeacherFilterForm
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .models import TeacherProfile, Review
from bookings.models import Booking


@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        messages.error(request, 'Access denied. Teacher privileges required.')
        return redirect('dashboard')

    teacher_profile = TeacherProfile.objects.get_or_create(user=request.user)[0]


    bookings = Booking.objects.filter(
        teacher=teacher_profile
    ).order_by('-created_at')

    teachers = TeacherProfile.objects.select_related('user').prefetch_related('skills').all()
    teacher_skills = TeacherSkill.objects.filter(teacher_profile=teacher_profile)
    reviews = Review.objects.filter(teacher_profile=teacher_profile)

    context = {
        'teacher_profile': teacher_profile,
        'teacher_skills': teacher_skills,
        'reviews': reviews,
        'featured_teachers': teachers,
        'total_teachers': teachers.count(),
        'bookings': bookings  # Add bookings to context
    }
    return render(request, 'teaching/dash_teacher.html', context)


@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Student privileges required.')
        return redirect('dashboard')

    # Get student's bookings
    bookings = Booking.objects.filter(
        student=request.user
    ).select_related('teacher__user').order_by('-created_at')

    # Count pending bookings
    pending_bookings = bookings.filter(status='PENDING').count()

    context = {
        'bookings': bookings,
        'pending_bookings': pending_bookings,
        'total_teachers': TeacherProfile.objects.count(),
        'featured_teachers': TeacherProfile.objects.select_related('user').all()[:4]
    }
    return render(request, 'teaching/dash_student.html', context)


def teacher_profile_view(request, teacher_id):
    teacher_profile = TeacherProfile.objects.get(id=teacher_id)
    reviews = Review.objects.filter(teacher_profile=teacher_profile).order_by('-created_at')

    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    review_count = reviews.count()

    context = {
        'teacher_profile': teacher_profile,
        'user': teacher_profile.user,
        'skills': teacher_profile.skills,
        'communication_methods': teacher_profile.communication_methods,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count': review_count,
    }
    return render(request, 'users/profile_teacher.html', context)


@login_required
def teacher_profile_edit(request):
    teacher_profile, created = TeacherProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = TeacherProfileForm(request.POST, instance=teacher_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('teacher_profile', teacher_id=teacher_profile.id)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = TeacherProfileForm(instance=teacher_profile)

    return render(request, 'teaching/teacher_profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def edit_student_profile(request):
    student, created = Student.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        student_form = StudentUpdateForm(request.POST, instance=student)

        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_student')
    else:
        user_form = UserUpdateForm(instance=request.user)
        student_form = StudentUpdateForm(instance=student)

    return render(request, 'teaching/student_profile_edit.html', {
        'user_form': user_form,
        'student_form': student_form,
    })


def search_teachers(request):
    query = request.GET.get('q', '').strip()
    if query:
        teachers = TeacherProfile.objects.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(skills__name__icontains=query)
        ).distinct()
    else:
        teachers = TeacherProfile.objects.none()

    return render(request, 'teaching/search_results.html', {'teachers': teachers, 'query': query})


def featured_teachers_view(request):
    try:
        all_teachers = TeacherProfile.objects.select_related('user').prefetch_related('skills').all()

        context = {
            'featured_teachers': all_teachers,
            'total_teachers': all_teachers.count()
        }

        return render(request, 'teaching/dash_teacher.html', context)
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return render(request, 'teaching/dash_teacher.html', {'featured_teachers': []})


def add_review(request, teacher_id):
    if request.method == 'POST':
        teacher = get_object_or_404(TeacherProfile, id=teacher_id)
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')
        Review.objects.create(
            teacher_profile=teacher,
            student=request.user,
            rating=rating,
            comment=comment
        )
        messages.success(request, 'Review added successfully!')
        return redirect('teacher_profile', teacher_id=teacher.id)


