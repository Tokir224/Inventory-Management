from django.db import models

from inventory_management.apps.raw_material.models import ProductRawMaterial
from inventory_management.apps.users.models import Shop
from inventory_management.constant import TYPE


class Product(models.Model):
    class Meta:
        db_table = 'product'

    name = models.CharField(max_length=100)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def to_dict_json(self, index):
        return {
            'index': index,
            'pk': self.pk,
            'name': self.name,
        }


class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(ProductRawMaterial, on_delete=models.CASCADE)
    amount = models.FloatField()
    type = models.IntegerField(choices=TYPE)

    class Meta:
        db_table = "product_ingredient"

    def to_dict_json(self, index):
        return {
            'index': index,
            'pk': self.product.id,
            'name': self.product.name,
        }
