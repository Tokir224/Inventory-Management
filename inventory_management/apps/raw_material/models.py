from django.db import models

from inventory_management.apps.stock.utills import CONVERTOR
from inventory_management.apps.users.models import Shop
from inventory_management.constant import PRODUCT_TYPE


def stock_with_type(product_type, amount):
    if product_type == 1:
        return f'{amount:.2f} KG'
    elif product_type == 2:
        return f'{amount:.2f} L'
    else:
        return f'{amount:.2f} Pieces'


class ProductRawMaterial(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    product_type = models.IntegerField(choices=PRODUCT_TYPE)
    min_stock = models.FloatField()

    class Meta:
        db_table = "raw_materials"

    def get_available_stock(self):
        from inventory_management.apps.stock.models import Stock
        stock_in = 0
        stock_out = 0
        stocks = Stock.objects.filter(raw_material=self)

        for stock in stocks:
            if stock.stock_type == 1:
                if stock.unit_type in CONVERTOR.keys():
                    convertor = CONVERTOR[stock.unit_type]()
                    stock_in += convertor.convert(stock.bulk)
                else:
                    stock_in += stock.bulk
            else:
                if stock.unit_type in CONVERTOR.keys():
                    convertor = CONVERTOR[stock.unit_type]()
                    stock_out += convertor.convert(stock.bulk)
                else:
                    stock_out += stock.bulk

        available_stock = stock_in - stock_out
        return available_stock

    def stock_status(self):
        if self.min_stock <= self.get_available_stock():
            return True
        else:
            return False

    def to_dict_json(self, index):
        return {
            'index': index,
            'pk': self.pk,
            'name': self.name,
            'min_stock': stock_with_type(self.product_type, self.min_stock),
            'available_stock': stock_with_type(self.product_type, self.get_available_stock()),
            'stocks': self.stock_status(),
            'product_type': self.product_type,
        }
