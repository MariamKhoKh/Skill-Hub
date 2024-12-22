from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:teacher_id>/', views.book_session, name='book_session'),
    path('respond/<int:booking_id>/', views.respond_to_booking, name='respond_booking'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/mark/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),]
