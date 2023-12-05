from django import forms

from inventory_management.apps.product.models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name']
