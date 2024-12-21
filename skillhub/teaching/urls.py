from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('profile-teacher/edit/', views.teacher_profile_edit, name='teacher_profile_edit'),
    path('teacher/<int:teacher_id>/', views.teacher_profile_view, name='teacher_profile'),
    path('profile-student/edit/',  views.edit_student_profile, name='edit_student_profile'),
]
