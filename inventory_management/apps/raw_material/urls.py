from django.urls import path

from .views import *

app_name = 'raw'

urlpatterns = [
    path("raw_material_create", RawMaterialCreateView.as_view(), name='raw_material_create'),
    path("raw_material_list", RawMaterialListView.as_view(), name='raw_material_list'),
    path("raw_material_update/<int:pk>", RawMaterialUpdateView.as_view(), name='raw_material_update'),
    path("raw_material_delete/<int:pk>", RawMaterialDeleteView.as_view(), name='raw_material_delete'),
    path('raw_material_list_data', raw_material_ajax_list, name='raw_material_list_data'),
]
