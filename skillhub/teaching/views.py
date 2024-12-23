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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TeacherProfileSerializer
from rest_framework.generics import ListAPIView


# @login_required
# def teacher_dashboard(request):
#     if request.user.role != 'teacher':
#         messages.error(request, 'Access denied. Teacher privileges required.')
#         return redirect('dashboard')
#
#     teacher_profile = TeacherProfile.objects.get_or_create(user=request.user)[0]
#
#
#     bookings = Booking.objects.filter(
#         teacher=teacher_profile
#     ).order_by('-created_at')
#
#     teachers = TeacherProfile.objects.select_related('user').prefetch_related('skills').all()
#     teacher_skills = TeacherSkill.objects.filter(teacher_profile=teacher_profile)
#     reviews = Review.objects.filter(teacher_profile=teacher_profile)
#
#     context = {
#         'teacher_profile': teacher_profile,
#         'teacher_skills': teacher_skills,
#         'reviews': reviews,
#         'featured_teachers': teachers,
#         'total_teachers': teachers.count(),
#         'bookings': bookings  # Add bookings to context
#     }
#     return render(request, 'teaching/dash_teacher.html', context)
#
#
# @login_required
# def student_dashboard(request):
#     if request.user.role != 'student':
#         messages.error(request, 'Access denied. Student privileges required.')
#         return redirect('dashboard')
#
#     # Get student's bookings
#     bookings = Booking.objects.filter(
#         student=request.user
#     ).select_related('teacher__user').order_by('-created_at')
#
#     # Count pending bookings
#     pending_bookings = bookings.filter(status='PENDING').count()
#
#     context = {
#         'bookings': bookings,
#         'pending_bookings': pending_bookings,
#         'total_teachers': TeacherProfile.objects.count(),
#         'featured_teachers': TeacherProfile.objects.select_related('user').all()[:4]
#     }
#     return render(request, 'teaching/dash_student.html', context)

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
    teachers = filter_teachers(request, teachers)  # Apply filtering

    teacher_skills = TeacherSkill.objects.filter(teacher_profile=teacher_profile)
    reviews = Review.objects.filter(teacher_profile=teacher_profile)

    context = {
        'teacher_profile': teacher_profile,
        'teacher_skills': teacher_skills,
        'reviews': reviews,
        'featured_teachers': teachers,
        'total_teachers': teachers.count(),
        'bookings': bookings
    }
    return render(request, 'teaching/dash_teacher.html', context)


@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Student privileges required.')
        return redirect('dashboard')

    bookings = Booking.objects.filter(
        student=request.user
    ).select_related('teacher__user').order_by('-created_at')

    pending_bookings = bookings.filter(status='PENDING').count()

    teachers = TeacherProfile.objects.select_related('user').all()
    teachers = filter_teachers(request, teachers)  # Apply filtering

    context = {
        'bookings': bookings,
        'pending_bookings': pending_bookings,
        'total_teachers': teachers.count(),
        'featured_teachers': teachers[:4]
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
        profile_form = TeacherProfileForm(request.POST, request.FILES, instance=teacher_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)

            # Process new skills
            new_skills_text = request.POST.get('new_skills', '')
            if new_skills_text:
                skill_names = [name.strip() for name in new_skills_text.split(',')]
                for skill_name in skill_names:
                    if skill_name:  # Only process non-empty skills
                        skill, _ = Skill.objects.get_or_create(name=skill_name)
                        profile.skills.add(skill)

            # Save the profile and many-to-many relationships
            profile.save()
            profile_form.save_m2m()

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


def dash(request):
    teachers_query = TeacherProfile.objects.all()
    teachers_query = filter_teachers(request, teachers_query)

    context = {
        'featured_teachers': teachers_query,
        'total_teachers': teachers_query.count(),
    }

    return render(request, 'teaching/dash_teacher.html', context)


class TeacherProfileView(APIView):
    def get(self, request, pk):
        teacher = TeacherProfile.objects.get(pk=pk)
        serializer = TeacherProfileSerializer(teacher)
        return Response(serializer.data)


class TeacherListView(ListAPIView):
    """
    View to list all teachers or filter them by skill.
    """
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer

    def get_queryset(self):
        """
        Override to filter teachers by skill if 'skill' parameter is provided.
        """
        queryset = super().get_queryset()
        skill = self.request.query_params.get('skill', None)
        if skill:
            queryset = queryset.filter(skills__name__icontains=skill)
        return queryset


class HighRatedTeachersView(ListAPIView):
    """
    View to list teachers with a minimum rating.
    """
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer

    def get_queryset(self):
        """
        Override to filter teachers by rating if 'min_rating' parameter is provided.
        """
        queryset = super().get_queryset()
        min_rating = self.request.query_params.get('min_rating', None)
        if min_rating:
            try:
                min_rating = float(min_rating)
                queryset = queryset.filter(rating__gte=min_rating)
            except ValueError:
                pass  # Ignore invalid values
        return queryset


def filter_teachers(request, teachers_query):
    experience = request.GET.get('experience')
    platforms = request.GET.getlist('platforms')
    rate = request.GET.get('rate')

    if experience:
        if experience == '1-3':
            teachers_query = teachers_query.filter(experience_years__gte=1, experience_years__lte=3)
        elif experience == '4-6':
            teachers_query = teachers_query.filter(experience_years__gte=4, experience_years__lte=6)
        elif experience == '7+':
            teachers_query = teachers_query.filter(experience_years__gte=7)

    if platforms:
        for platform in platforms:
            teachers_query = teachers_query.filter(communication_methods__icontains=platform)

    if rate:
        try:
            rate_value = float(rate)
            teachers_query = teachers_query.filter(hourly_rate__lte=rate_value)
        except ValueError:
            pass

    return teachers_query



