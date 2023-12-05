from django import forms

from inventory_management.apps.stock.models import Stock
from inventory_management.constant import TYPE


class StockForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        product_type = kwargs.pop('product_type')
        super().__init__(*args, **kwargs)
        if product_type == 1:
            self.fields['unit_type'].choices = TYPE[:3]
        elif product_type == 2:
            self.fields['unit_type'].choices = TYPE[3:5]
        elif product_type == 3:
            self.fields['unit_type'].choices = TYPE[5:]

    class Meta:
        model = Stock
        exclude = ['raw_material', 'stock_type', 'created_at']
