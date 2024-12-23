from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm
from .models import User, Message, Notification
from teaching.models import TeacherProfile
from django.db.models import Avg
from django.views.decorators.cache import cache_page


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')

            # Redirect based on the role
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required
def dashboard(request):
    if request.user.role == 'student':
        return redirect('student_dashboard')
    elif request.user.role == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('login')


@login_required
def profile_student(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_student')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile_student.html', {'form': form})


@login_required
@cache_page(60 * 15)
def profile_teacher(request):
    teacher = TeacherProfile.objects.get(user=request.user)
    reviews = teacher.reviews.all().order_by('-created_at')  # Assuming a `Review` model with a `created_at` field
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    review_count = reviews.count()

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_teacher')
    else:
        form = UserUpdateForm(instance=request.user)
        context = {
            'form': form,
            'teacher_profile': teacher,
            'reviews': reviews,
            'avg_rating': round(avg_rating, 1),
            'review_count': review_count,
        }
    return render(request, 'users/profile_teacher.html', context)


def navbar_data(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')[:5]
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')[:5]
    return {'messages': messages, 'notifications': notifications}








