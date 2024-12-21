from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import TeacherProfile, Skill, TeacherSkill, Review, Student
from .forms import TeacherProfileForm, TeacherSkillForm, ReviewForm, TeacherSearchForm, StudentUpdateForm, StudentProfileUpdateForm
from users.models import User

from users.forms import UserUpdateForm


@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        messages.error(request, 'Access denied. Teacher privileges required.')
        return redirect('dashboard')

    teacher_profile = TeacherProfile.objects.get_or_create(user=request.user)[0]
    teacher_skills = TeacherSkill.objects.filter(teacher_profile=teacher_profile)
    reviews = Review.objects.filter(teacher_profile=teacher_profile)

    context = {
        'teacher_profile': teacher_profile,
        'teacher_skills': teacher_skills,
        'reviews': reviews,
    }
    return render(request, 'teaching/dash_teacher.html', context)


# @login_required
# def student_dashboard(request):
#     if request.user.role != 'student':
#         messages.error(request, 'Access denied. Seems you are not student')
#         return redirect('dash_student')
#
#     form = TeacherSearchForm(request.GET)
#     teachers = TeacherProfile.objects.all()
#
#     if form.is_valid():
#         search_query = form.cleaned_data.get('search_query')
#         min_price = form.cleaned_data.get('min_price')
#         max_price = form.cleaned_data.get('max_price')
#         min_rating = form.cleaned_data.get('min_rating')
#
#         if search_query:
#             teachers = teachers.filter(
#                 Q(user__username__icontains=search_query) |
#                 Q(skills__name__icontains=search_query)
#             ).distinct()
#
#         if min_price is not None:
#             teachers = teachers.filter(hourly_rate__gte=min_price)
#         if max_price is not None:
#             teachers = teachers.filter(hourly_rate__lte=max_price)
#         if min_rating is not None:
#             teachers = teachers.filter(rating__gte=min_rating)
#
#     context = {
#         'form': form,
#         'teachers': teachers,
#     }
#     return render(request, 'teaching/dash_student.html', context)

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Seems you are not student')
        return redirect('dashboard')

    form = TeacherSearchForm(request.GET)
    teachers = TeacherProfile.objects.all()

    if form.is_valid():
        # Search query filter
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            teachers = teachers.filter(
                Q(user__username__icontains=search_query) |
                Q(skills__icontains=search_query) |
                Q(bio__icontains=search_query)
            ).distinct()

        # Experience range filter
        experience_range = form.cleaned_data.get('experience_range')
        if experience_range:
            if experience_range == '1-3':
                teachers = teachers.filter(experience_years__gte=1, experience_years__lte=3)
            elif experience_range == '4-6':
                teachers = teachers.filter(experience_years__gte=4, experience_years__lte=6)
            elif experience_range == '7+':
                teachers = teachers.filter(experience_years__gte=7)

        # Price range filter
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        if min_price is not None:
            teachers = teachers.filter(hourly_rate__gte=min_price)
        if max_price is not None:
            teachers = teachers.filter(hourly_rate__lte=max_price)

        # Rating filter
        min_rating = form.cleaned_data.get('min_rating')
        if min_rating is not None:
            teachers = teachers.filter(rating__gte=min_rating)

        # Communication methods filter
        communication_methods = form.cleaned_data.get('communication_method')
        if communication_methods:
            q_objects = Q()
            for method in communication_methods:
                q_objects |= Q(communication_methods__icontains=method)
            teachers = teachers.filter(q_objects)

    context = {
        'form': form,
        'teachers': teachers,
    }
    return render(request, 'teaching/dash_student.html', context)


@login_required
def teacher_profile_view(request, teacher_id):
    teacher_profile = TeacherProfile.objects.get(id=teacher_id)
    context = {
        'teacher_profile': teacher_profile,
        'user': teacher_profile.user,
        'skills': teacher_profile.get_skills(),
        'communication_methods': teacher_profile.communication_methods_list()
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
    student, created = Student.objects.get_or_create(
        user=request.user,
        defaults={
            'grade': '',
            'track': '',
        }
    )
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

    return render(request, 'users/profile_student.html', {
        'user_form': user_form,
        'student_form': student_form
    })