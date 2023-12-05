from inventory_management.apps.notification.models import Notifications


def show_notification(request):
    if request.user.is_authenticated:
        notifications = Notifications.objects.filter(shop=request.user.shop, is_read=False).order_by('-created_at')
        is_read = True
        for notification in notifications:
            if notification.is_read is False:
                is_read = False
        return {'notifications': notifications, 'is_read': is_read}
    else:
        return {'notifications': '', 'is_read': ''}
