from django.urls import path
from . import views
from .views import TeacherProfileView, TeacherListView, HighRatedTeachersView

urlpatterns = [
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('profile-teacher/edit/', views.teacher_profile_edit, name='teacher_profile_edit'),
    path('teacher/<int:teacher_id>/', views.teacher_profile_view, name='teacher_profile'),
    path('profile-student/edit/',  views.edit_student_profile, name='edit_student_profile'),
    path('search/', views.search_teachers, name='search_teachers'),
    path('featured-teachers/', views.featured_teachers_view, name='featured_teachers'),
    path('add-review/<int:teacher_id>/', views.add_review, name='add_review'),
    path('api/teachers/', TeacherListView.as_view(), name='teachers_list'),
    path('api/teachers/<int:pk>/', TeacherProfileView.as_view(), name='teacher_profile_api'),
    path('api/teachers/high-rated/', HighRatedTeachersView.as_view(), name='high_rated_teachers'),

]
