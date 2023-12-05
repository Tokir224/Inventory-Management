import math

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView

from inventory_management.apps.raw_material.forms import ProductRawMaterialForm
from inventory_management.apps.raw_material.models import ProductRawMaterial


class RawMaterialCreateView(LoginRequiredMixin, CreateView):
    model = ProductRawMaterial
    form_class = ProductRawMaterialForm
    template_name = "raw_material/create.html"
    success_url = reverse_lazy('raw:raw_material_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.shop = self.request.user.shop
        obj.save()
        return super().form_valid(form)


class RawMaterialListView(LoginRequiredMixin, TemplateView):
    template_name = 'raw_material/list.html'


@login_required(login_url=reverse_lazy('admin_user:login'))
def raw_material_ajax_list(request):
    if request.method == "GET":

        raw_material_list = ProductRawMaterial.objects.filter(shop=request.user.shop)

        if request.GET.get('search[value]') != "":
            search = request.GET.get('search[value]')
            raw_material_list = raw_material_list.filter(Q(name__icontains=search))

        total = raw_material_list.count()
        _start = request.GET.get('start')
        _length = request.GET.get('length')
        page = 0
        per_page = 0
        if _start and _length:
            start = int(_start)
            length = int(_length)

            page = math.ceil(start / length) + 1
            per_page = length

            raw_material_list = raw_material_list[start:start + length]

        data = [raw_material_data.to_dict_json(index) for index, raw_material_data in
                enumerate(raw_material_list, start=1)]

        response = {
            'data': data,
            'page': page,
            'per_page': per_page,
            'recordsTotal': total,
            'recordsFiltered': total,
        }
        return JsonResponse(response)


class RawMaterialUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductRawMaterial
    form_class = ProductRawMaterialForm
    template_name = "raw_material/create.html"
    success_url = reverse_lazy('raw:raw_material_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.shop = self.request.user.shop
        obj.save()
        return super().form_valid(form)


class RawMaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductRawMaterial
    success_url = reverse_lazy('raw:raw_material_list')



