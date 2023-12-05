from django import forms

from inventory_management.apps.raw_material.models import ProductRawMaterial


class ProductRawMaterialForm(forms.ModelForm):
    min_stock = forms.FloatField(widget=forms.NumberInput, min_value=1.0)

    class Meta:
        model = ProductRawMaterial
        exclude = ['shop']
