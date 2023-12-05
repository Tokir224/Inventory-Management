from django.urls import path

from .views import *

app_name = 'stock'

urlpatterns = [
    path("stocks", StockView.as_view(), name='stocks'),
    path("stock_list/<int:pk>", StockListView.as_view(), name='stock_list'),
    path('stock_list_data/<int:pk>', stock_ajax_list, name='stock_list_data'),
    path('stock_add/<int:pk>', StockAddView.as_view(), name='stock_add'),
    path('stock_remove/<int:pk>', StockRemoveView.as_view(), name='stock_remove'),

    path('stock_consumption', StockConsumptionView.as_view(), name='stock_consumption'),
    path('stock_raw_sale', StockRawMaterialSalesView.as_view(), name='stock_raw_sale'),
    path('stock_product_sale', StockProductSalesView.as_view(), name='stock_product_sale'),
]
