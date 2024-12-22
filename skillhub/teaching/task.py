from celery import shared_task
from django.core.mail import send_mail
from .models import Booking


@shared_task
def send_booking_confirmation(booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        subject = "Lesson Booking Confirmation"
        message = f"Dear {booking.student.username},\n\nYou have successfully booked the lesson '{booking.lesson.title}' on {booking.lesson.date}."
        recipient_list = [booking.student.email]
        send_mail(subject, message, 'no-reply@skillhub.com', recipient_list)
    except Booking.DoesNotExist:
        pass  # Log error if needed
