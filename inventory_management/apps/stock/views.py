import math

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from inventory_management.apps.product.models import Product, ProductIngredient
from inventory_management.apps.raw_material.models import ProductRawMaterial
from inventory_management.apps.stock.forms import StockForm
from inventory_management.apps.stock.models import Stock
from inventory_management.apps.stock.utills import CONVERTOR


class StockView(LoginRequiredMixin, TemplateView):
    template_name = 'stock/list.html'


class StockListView(LoginRequiredMixin, TemplateView):
    template_name = 'stock/stock_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['pk'] = kwargs['pk']
        return context


@login_required(login_url=reverse_lazy('admin_user:login'))
def stock_ajax_list(request, pk):
    if request.method == "GET":
        stock_list = Stock.objects.filter(raw_material_id=pk).order_by('-created_at')

        if request.GET.get('search[value]') != "":
            search = request.GET.get('search[value]')
            stock_list = stock_list.filter(Q(raw_material__name__icontains=search))

        total = stock_list.count()
        _start = request.GET.get('start')
        _length = request.GET.get('length')
        page = 0
        per_page = 0
        if _start and _length:
            start = int(_start)
            length = int(_length)

            page = math.ceil(start / length) + 1
            per_page = length

            stock_list = stock_list[start:start + length]

        data = [stock_list_data.to_dict_json(index) for index, stock_list_data in
                enumerate(stock_list, start=1)]
        response = {
            'data': data,
            'page': page,
            'per_page': per_page,
            'recordsTotal': total,
            'recordsFiltered': total,
        }
        return JsonResponse(response)


class StockAddView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        raw_material = ProductRawMaterial.objects.get(pk=kwargs['pk'])
        form = StockForm(product_type=raw_material.product_type)
        return render(request, 'stock/add.html', {'form': form})

    def post(self, request, *args, **kwargs):
        raw_material_id = kwargs['pk']
        raw_material = ProductRawMaterial.objects.get(pk=raw_material_id)
        form = StockForm(request.POST, product_type=raw_material.product_type)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.raw_material = raw_material
            obj.stock_type = 1
            obj.save()
            messages.success(request, 'Raw material quantity added')
            return redirect(reverse_lazy('raw:raw_material_list'))
        else:
            messages.error(request, 'Something went wrong')
            return render(request, 'stock/add.html', {'form': form})


class StockRemoveView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        raw_material = ProductRawMaterial.objects.get(pk=kwargs['pk'])
        form = StockForm(product_type=raw_material.product_type)
        return render(request, 'stock/remove.html', {'form': form})

    def post(self, request, *args, **kwargs):
        raw_material_id = kwargs['pk']
        raw_material = ProductRawMaterial.objects.get(pk=raw_material_id)
        form = StockForm(request.POST, product_type=raw_material.product_type)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.raw_material = raw_material
            obj.stock_type = 2
            if obj.unit_type in CONVERTOR.keys():
                convertor = CONVERTOR[obj.unit_type]()
                total = convertor.convert(obj.bulk)
            else:
                total = obj.bulk

            if total > raw_material.get_available_stock():
                messages.error(request, "Raw material quantity Not available")
                return redirect(reverse_lazy('raw:raw_material_list'))
            obj.save()

            messages.success(request, 'Raw material quantity Removed')
            return redirect(reverse_lazy('raw:raw_material_list'))
        else:
            messages.error(request, 'Something went wrong')
            return render(request, 'stock/add.html', {'form': form})


class StockConsumptionView(LoginRequiredMixin, TemplateView):
    template_name = 'stock/consumption.html'


class StockRawMaterialSalesView(LoginRequiredMixin, View):

    def post(self, request):
        raw_material_id = int(request.POST.get("pk"))
        bulk = int(request.POST.get("bulk"))
        unit_type = int(request.POST.get("unit_type"))

        raw_material = ProductRawMaterial.objects.get(pk=raw_material_id)

        if unit_type in CONVERTOR.keys():
            convertor = CONVERTOR[unit_type]()
            total = convertor.convert(bulk)
        else:
            total = bulk

        if total > raw_material.get_available_stock():
            messages.error(request, "Raw material quantity Not available")
            data = {"status": 201}
            return JsonResponse(data)

        Stock.objects.create(raw_material=raw_material,
                             bulk=bulk,
                             unit_type=unit_type,
                             stock_type=2,
                             )

        messages.success(request, 'Raw material quantity Removed')
        data = {"status": 200}
        return JsonResponse(data)


class StockProductSalesView(LoginRequiredMixin, View):
    def post(self, request):
        product_id = int(request.POST.get("pk"))
        product_quantity = int(request.POST.get("product_quantity"))

        product = Product.objects.get(pk=product_id)

        product_ingredients = ProductIngredient.objects.filter(product=product)

        all_objects = []

        for product_ingredient in product_ingredients:
            if product_ingredient.type in CONVERTOR.keys():
                convertor = CONVERTOR[product_ingredient.type]()
                total = convertor.convert(product_ingredient.amount) * product_quantity
            else:
                total = product_ingredient.amount * product_quantity

            if total > product_ingredient.raw_material.get_available_stock():
                messages.error(request, "Raw material quantity Not available")
                data = {"status": 201}
                return JsonResponse(data)

            all_objects.append(Stock(raw_material=product_ingredient.raw_material,
                                     bulk=product_ingredient.amount,
                                     unit_type=product_ingredient.type,
                                     stock_type=2,
                                     ))

        for obj in all_objects:
            obj.save()

        messages.success(request, 'Raw material quantity Removed')
        data = {"status": 200}
        return JsonResponse(data)
