"""inventory_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .settings import settings
from inventory_management.apps.notification.cron import send_notification

urlpatterns = [
                  path("main_admin/", admin.site.urls),
                  path('', include('inventory_management.apps.users.urls')),
                  path('', include('inventory_management.apps.dashboard.urls')),
                  path('admin/', include('inventory_management.apps.product.urls')),
                  path('admin/', include('inventory_management.apps.raw_material.urls')),
                  path('admin/', include('inventory_management.apps.stock.urls')),
                  path('admin/', include('inventory_management.apps.notification.urls')),
                  path('admin/notification', send_notification),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
