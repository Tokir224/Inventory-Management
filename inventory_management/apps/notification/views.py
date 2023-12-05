from django.shortcuts import redirect

from inventory_management.apps.notification.models import Notifications


def notification_detail(request, pk):
    if request.method == 'GET':
        notification = Notifications.objects.get(pk=pk)
        notification.is_read = True
        notification.save()
        return redirect('stock:stocks')
