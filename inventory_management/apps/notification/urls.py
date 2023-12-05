from django.urls import path

from .views import *

app_name = 'notification'

urlpatterns = [
    path("notification_detail/<int:pk>", notification_detail, name='notification_detail'),
]