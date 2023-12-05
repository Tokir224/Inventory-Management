from django.db import models

from inventory_management.apps.users.models import Shop


class Notifications(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
