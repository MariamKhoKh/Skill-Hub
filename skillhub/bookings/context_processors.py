from .models import Notification


def unread_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, is_read=False)
        return {'notifications': notifications}
    return {'notifications': []}
