from celery import shared_task
from django.core.mail import send_mail
from .models import Booking, Notification


@shared_task
def send_notification_to_teacher(booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        teacher = booking.teacher.user
        print(f"Found booking and teacher: {teacher.email}")

        Notification.objects.create(
            recipient=teacher,
            title="New Booking Request",
            message=f"""
            You have a new booking request from {booking.student.username}.
            Topic: {booking.topic}
            Date and Time: {booking.date_time}
            Duration: {booking.duration} hours
            """
        )

        # Send email notification
        subject = "New Booking Request"
        message = f"""
        You have a new booking request from {booking.student.username}.
        Topic: {booking.topic}
        Date and Time: {booking.date_time}
        Duration: {booking.duration} hours
        """
        send_mail(subject, message, 'admin@skillhub.com', [teacher.email])
        print("Email sent successfully")

    except Booking.DoesNotExist:
        pass


@shared_task
def send_notification_to_student(booking_id):
    try:
        booking = Booking.objects.select_related('teacher__user', 'student').get(id=booking_id)
        student = booking.student

        # Create notification message based on status
        if booking.status == 'ACCEPTED':
            title = "Booking Accepted!"
            message = f"""Your booking request with {booking.teacher.user.username} has been accepted!
                         Date: {booking.date_time.strftime('%B %d, %Y %H:%M')}
                         Topic: {booking.topic}"""
        else:
            title = "Booking Rejected"
            message = f"""Your booking request with {booking.teacher.user.username} was rejected.
                         Reason: {booking.rejection_reason}
                         You can make a new booking with another teacher."""

        # Create notification in database
        Notification.objects.create(
            recipient=student,
            title=title,
            message=message
        )

        # Send email notification
        send_mail(
            subject=title,
            message=message,
            from_email='admin@skillhub.com',
            recipient_list=[student.email]
        )

    except Booking.DoesNotExist:
        pass