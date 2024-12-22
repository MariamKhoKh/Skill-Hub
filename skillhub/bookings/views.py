from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking, Notification
from teaching.models import TeacherProfile
from .task import send_notification_to_teacher, send_notification_to_student
from django.utils import timezone


@login_required
def book_session(request, teacher_id):
    teacher = get_object_or_404(TeacherProfile, id=teacher_id)

    if request.method == 'POST':
        date_time_str = request.POST.get('date_time')
        try:
            # Parse ISO format datetime string
            date_time = timezone.make_aware(datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M'))
        except ValueError:
            messages.error(request, "Invalid date format")
            return render(request, 'booking/book_session.html', {'teacher': teacher})

        duration = request.POST.get('duration')
        topic = request.POST.get('topic')

        # Create the booking instance
        booking = Booking.objects.create(
            student=request.user,
            teacher=teacher,
            date_time=date_time,
            duration=duration,
            topic=topic
        )

        # Notify the teacher asynchronously
        send_notification_to_teacher.delay(booking.id)

        messages.success(request, "Your booking has been submitted!")
        return redirect('teacher_profile', teacher_id=teacher_id)

    return render(request, 'booking/book_session.html', {'teacher': teacher})


@login_required
def respond_to_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, teacher__user=request.user)

    if request.method == 'POST':
        status = request.POST.get('status')
        rejection_reason = request.POST.get('rejection_reason', '')

        if status == 'ACCEPTED':
            booking.status = 'ACCEPTED'
        elif status == 'REJECTED':
            booking.status = 'REJECTED'
            booking.rejection_reason = rejection_reason

        booking.save()

        # Notify the student about the teacher's response
        send_notification_to_student.delay(booking.id)

        messages.success(request, "Your response has been recorded.")
        return redirect('teacher_dashboard')

    return render(request, 'booking/respond_booking.html', {'booking': booking})


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).order_by('-timestamp')
    return JsonResponse({
        'notifications': list(notifications.values('id', 'title', 'message', 'timestamp'))
    })


# @login_required
# def get_notifications(request):
#     notifications = Notification.objects.filter(
#         recipient=request.user,
#         is_read=False
#     ).order_by('-timestamp')
#
#     return JsonResponse({
#         'notifications': [{
#             'id': notification.id,
#             'title': notification.title,
#             'message': notification.message,
#             'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')
#         } for notification in notifications]
#     })


@login_required
def mark_notification_read(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(
            Notification,
            id=notification_id,
            recipient=request.user
        )
        notification.is_read = True
        notification.save()

        # Get updated unread count
        unread_count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()

        return JsonResponse({
            'status': 'success',
            'unread_count': unread_count
        })
    return JsonResponse({'status': 'error'}, status=400)




