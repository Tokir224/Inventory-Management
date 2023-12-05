from django.db import models

from inventory_management.apps.raw_material.models import ProductRawMaterial
from inventory_management.constant import TYPE, STOCK


class Stock(models.Model):
    raw_material = models.ForeignKey(ProductRawMaterial, on_delete=models.CASCADE)
    bulk = models.FloatField()
    unit_type = models.IntegerField(choices=TYPE)
    stock_type = models.IntegerField(choices=STOCK)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = "stocks"

    def to_dict_json(self, index):
        return {
            'index': index,
            'pk': self.pk,
            'raw_material': self.raw_material.name,
            'bulk': self.bulk,
            'unit_type': TYPE[self.unit_type - 1][1],
            'stock_type': STOCK[self.stock_type - 1][1],
        }
