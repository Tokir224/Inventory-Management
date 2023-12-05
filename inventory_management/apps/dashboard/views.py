from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from inventory_management.apps.product.models import Product
from inventory_management.apps.raw_material.models import ProductRawMaterial
from inventory_management.apps.users.models import Users


@login_required(login_url=reverse_lazy("admin_user:login"))
def dashboard(request):
    users = Users.objects.filter(shop=request.user.shop).count()
    products = Product.objects.filter(shop=request.user.shop).count()
    raw_materials = ProductRawMaterial.objects.filter(shop=request.user.shop).count()
    return render(request, 'index.html', {'users': users, 'raw_materials': raw_materials, 'products': products})
