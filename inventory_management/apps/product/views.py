import math

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView

from inventory_management.apps.product.forms import ProductForm
from inventory_management.apps.product.models import Product, ProductIngredient
from inventory_management.apps.raw_material.models import ProductRawMaterial
from inventory_management.constant import TYPE


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/create.html"
    success_url = reverse_lazy('product:product_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.shop = self.request.user.shop
        obj.save()
        return super().form_valid(form)


class ProductListView(LoginRequiredMixin, TemplateView):
    template_name = 'products/list.html'


@login_required(login_url=reverse_lazy('admin_user:login'))
def product_ajax_list(request):
    if request.method == "GET":

        product_list = Product.objects.filter(shop=request.user.shop)

        if request.GET.get('search[value]') != "":
            search = request.GET.get('search[value]')
            product_list = product_list.filter(Q(name__icontains=search))

        total = product_list.count()
        _start = request.GET.get('start')
        _length = request.GET.get('length')
        page = 0
        per_page = 0
        if _start and _length:
            start = int(_start)
            length = int(_length)

            page = math.ceil(start / length) + 1
            per_page = length

            product_list = product_list[start:start + length]

        data = [product_data.to_dict_json(index) for index, product_data in enumerate(product_list, start=1)]
        response = {
            'data': data,
            'page': page,
            'per_page': per_page,
            'recordsTotal': total,
            'recordsFiltered': total,
        }
        return JsonResponse(response)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/create.html"
    success_url = reverse_lazy('product:product_list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product:product_list')


class ProductIngredientListView(LoginRequiredMixin, TemplateView):
    template_name = 'products_ingredient/list.html'


@login_required(login_url=reverse_lazy('admin_user:login'))
def product_ingredient_ajax_list(request):
    if request.method == "GET":
        product_list = list(Product.objects.filter(shop=request.user.shop).values_list('id', flat=True))
        product_ingredient_list = list(
            set(ProductIngredient.objects.filter(product_id__in=product_list).values_list('product_id', flat=True)))
        product_ingredient_list = Product.objects.filter(id__in=product_ingredient_list)

        if request.GET.get('search[value]') != "":
            search = request.GET.get('search[value]')
            product_ingredient_list = product_ingredient_list.filter(Q(name__icontains=search))

        total = product_ingredient_list.count()
        _start = request.GET.get('start')
        _length = request.GET.get('length')
        page = 0
        per_page = 0
        if _start and _length:
            start = int(_start)
            length = int(_length)

            page = math.ceil(start / length) + 1
            per_page = length

            product_ingredient_list = product_ingredient_list[start:start + length]

        data = [product_data.to_dict_json(index) for index, product_data in enumerate(product_ingredient_list, start=1)]
        response = {
            'data': data,
            'page': page,
            'per_page': per_page,
            'recordsTotal': total,
            'recordsFiltered': total,
        }
        return JsonResponse(response)


class ProductIngredientCreateView(LoginRequiredMixin, CreateView):

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(shop=request.user.shop)
        raw_materials = ProductRawMaterial.objects.filter(shop=request.user.shop)

        types = []
        for i in TYPE:
            types.append({'id': i[0], 'type': i[1]})
        return render(request, 'products_ingredient/create.html',
                      {'products': products, 'raw_materials': raw_materials, 'types': types})

    def post(self, request, *args, **kwargs):
        product = request.POST.get('product')
        raw_materials = request.POST.getlist('raw-material[]')
        amounts = request.POST.getlist('amount[]')
        unit_type = request.POST.getlist('type[]')

        for raw, amount, qu_type in tuple(zip(raw_materials, amounts, unit_type)):
            raw, amount, qu_type = int(raw), float(amount), int(qu_type)
            product_ingredient = ProductIngredient.objects.create(product_id=product,
                                                                  raw_material_id=raw,
                                                                  amount=amount,
                                                                  type=qu_type,
                                                                  )
            product_ingredient.save()

        messages.success(request, 'Product ingredient Saved Successfully')

        return redirect(reverse_lazy('product:product_ingredient_list'))


class ProductIngredientUpdateView(LoginRequiredMixin, UpdateView):

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(shop=request.user.shop)
        raw_materials = ProductRawMaterial.objects.filter(shop=request.user.shop)
        product_ingredients_old = ProductIngredient.objects.filter(product_id=kwargs['pk'])
        selected_product = Product.objects.get(id=kwargs['pk'])

        product_ingredients = []
        for product_ingredient in product_ingredients_old:
            if product_ingredient.raw_material.product_type == 1:
                product_type = TYPE[:3]
            elif product_ingredient.raw_material.product_type == 2:
                product_type = TYPE[3:5]
            else:
                product_type = TYPE[5:]

            types = []
            for i in product_type:
                types.append({'id': i[0], 'type': i[1]})

            product_ingredients.append({'product': product_ingredient.product,
                                        'raw_material': product_ingredient.raw_material,
                                        'amount': product_ingredient.amount,
                                        'type': product_ingredient.type,
                                        'types': types
                                        })

        return render(request, 'products_ingredient/update.html',
                      {'products': products, 'raw_materials': raw_materials, 'types': types,
                       'product_ingredients': product_ingredients, 'selected_product': selected_product})

    def post(self, request, *args, **kwargs):
        product = request.POST.get('product')
        raw_materials = request.POST.getlist('raw-material[]')
        amounts = request.POST.getlist('amount[]')
        unit_type = request.POST.getlist('type[]')

        product_ingredients = ProductIngredient.objects.filter(product_id=kwargs['pk'])
        for product_ingredient in product_ingredients:
            product_ingredient.delete()

        for raw, amount, qu_type in tuple(zip(raw_materials, amounts, unit_type)):
            raw, amount, qu_type = int(raw), float(amount), int(qu_type)
            product_ingredient = ProductIngredient.objects.create(product_id=product,
                                                                  raw_material_id=raw,
                                                                  amount=amount,
                                                                  type=qu_type,
                                                                  )
            product_ingredient.save()

        messages.success(request, 'Product ingredient Saved Successfully')

        return redirect(reverse_lazy('product:product_ingredient_list'))


class ProductIngredientDeleteView(LoginRequiredMixin, DeleteView):

    def post(self, request, *args, **kwargs):
        product_ingredients = ProductIngredient.objects.filter(product_id=kwargs['pk'])
        for product_ingredient in product_ingredients:
            product_ingredient.delete()

        return redirect(reverse_lazy('product:product_ingredient_list'))


def check_raw_material_type(request):
    raw_material_id = request.GET.get('raw_material_id')
    data = {"product_type": ProductRawMaterial.objects.get(id=raw_material_id).product_type}
    return JsonResponse(data)
