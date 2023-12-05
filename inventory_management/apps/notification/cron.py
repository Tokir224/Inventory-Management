from inventory_management.apps.notification.models import Notifications
from inventory_management.apps.raw_material.models import ProductRawMaterial


def send_notification(request):
    raw_materials = ProductRawMaterial.objects.all()

    for raw_material in raw_materials:
        if raw_material.min_stock > raw_material.get_available_stock():
            message = f'{raw_material.name} is out of stock'
            Notifications.objects.create(shop=raw_material.shop, message=message)
