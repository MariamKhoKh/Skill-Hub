from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile-student/', views.profile_student, name='profile_student'),
    path('profile-teacher/', views.profile_teacher, name='profile_teacher'),
]