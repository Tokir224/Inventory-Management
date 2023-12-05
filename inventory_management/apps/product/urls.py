from django.urls import path

from .views import *

app_name = 'product'

urlpatterns = [
    path("product_create", ProductCreateView.as_view(), name='product_create'),
    path("product_list", ProductListView.as_view(), name='product_list'),
    path("product_update/<int:pk>", ProductUpdateView.as_view(), name='product_update'),
    path("product_delete/<int:pk>", ProductDeleteView.as_view(), name='product_delete'),
    path('product_list_data', product_ajax_list, name='product_list_data'),

    path("product_ingredient_list", ProductIngredientListView.as_view(), name='product_ingredient_list'),
    path('product_ingredient_list_data', product_ingredient_ajax_list, name='product_ingredient_list_data'),
    path('product_ingredient_create', ProductIngredientCreateView.as_view(), name='product_ingredient_create'),
    path('product_ingredient_update/<int:pk>', ProductIngredientUpdateView.as_view(), name='product_ingredient_update'),
    path('product_ingredient_delete/<int:pk>', ProductIngredientDeleteView.as_view(), name='product_ingredient_delete'),

    path("raw_material_type", check_raw_material_type, name='raw_material_type')
]
