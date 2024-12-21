from .models import Message, Notification


def navbar_data(request):
    if request.user.is_authenticated:
        messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')[:5]
        notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')[:5]
        return {'messages': messages, 'notifications': notifications}
    return {}