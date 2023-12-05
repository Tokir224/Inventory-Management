import math
import csv

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, UpdateView, DeleteView, CreateView, FormView
from django.db.models import Q
from django.http import JsonResponse, HttpResponse

from .forms import UserEditForm, UserLoginForm, PwdResetConfirmForm, PwdResetForm, RegistrationForm
from .models import Users
from .tasks import set_password_link_mail_task, credential_mail_task


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    model = Users
    form_class = UserEditForm
    template_name = "profile/edit_details.html"
    success_message = "Profile has been updated"
    success_url = reverse_lazy('dashboard:dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class SignIn(View):

    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff is True:
            return redirect(reverse_lazy("dashboard:dashboard"))

        else:
            form = UserLoginForm()
            return render(request, "login.html", {'form': form})

    def post(self, request):
        user_email = request.POST.get("email")
        user_password = request.POST.get("password")

        user = authenticate(request, email=user_email, password=user_password, is_active=True)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect(reverse_lazy('dashboard:dashboard'))

        else:
            messages.error(request, "User Name Does Not Exists Or Password is Wrong.")
            url = reverse_lazy('admin_user:login')
            return redirect(url)


class PasswordResetConfirmView(View):
    form_class = PwdResetConfirmForm
    template_name = 'profile/password_reset_confirm.html',

    def get(self, request, **kwargs):
        form = PwdResetConfirmForm()
        return render(request, 'profile/password_reset_confirm.html', {'form': form})

    def post(self, request, **kwargs):
        form = PwdResetConfirmForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('new_password2')
            try:
                uid = force_str(urlsafe_base64_decode(kwargs['uidb64']))
                user = Users.objects.get(pk=uid)
            except:
                user = None
            if user is not None and default_token_generator.check_token(user, kwargs['token']):
                user.set_password(password)
                user.save()
                messages.success(request, 'Password changed successfully')
                return redirect(reverse_lazy('admin_user:login'))
        else:
            return render(request, 'profile/password_reset_confirm.html', {'form': form})


class PasswordResetView(View):
    template_name = "profile/password_reset_form.html",
    email_template_name = 'profile/password_reset_email.html',
    form_class = PwdResetForm

    def get(self, request):
        form = PwdResetForm()
        return render(request, "profile/password_reset_form.html", {'form': form})

    def post(self, request):
        form = PwdResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = Users.objects.filter(email=email).first()
            to_email = user.email
            uid = urlsafe_base64_encode(force_bytes(user.id))
            current_site = get_current_site(request).domain
            activation_link = "http://" + f"{current_site}/admin/password_reset_confirm/{uid}/" \
                                          f"{default_token_generator.make_token(user)} "

            # sending mail with celery
            set_password_link_mail_task.delay(activation_link, to_email, user.id)
            messages.success(request, 'Check your email to reset your password')
            return redirect(reverse_lazy('admin_user:login'))
        else:
            messages.error(request, 'This email is not exists')
            return render(request, "profile/password_reset_form.html", {'form': form})


class UserListView(LoginRequiredMixin, TemplateView):
    template_name = 'users/list.html'


@login_required(login_url=reverse_lazy('admin_user:login'))
def user_ajax_list(request):
    if request.method == "GET":

        user_list = Users.objects.filter(shop=request.user.shop, is_superuser=False)

        if request.GET.get('search[value]') != "":
            search = request.GET.get('search[value]')
            user_list = user_list.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search)
                                         | Q(email__icontains=search))

        total = user_list.count()
        _start = request.GET.get('start')
        _length = request.GET.get('length')
        page = 0
        per_page = 0
        if _start and _length:
            start = int(_start)
            length = int(_length)

            page = math.ceil(start / length) + 1
            per_page = length

            user_list = user_list[start:start + length]

        data = [user_data.to_dict_json(index) for index, user_data in enumerate(user_list, start=1)]
        response = {
            'data': data,
            'page': page,
            'per_page': per_page,
            'recordsTotal': total,
            'recordsFiltered': total,
        }
        return JsonResponse(response)


class UserCreateView(SuccessMessageMixin, CreateView):
    model = Users
    form_class = RegistrationForm
    template_name = "users/create.html"
    success_message = "User Created successfully"
    success_url = reverse_lazy('admin_user:user_list')

    def form_valid(self, form):
        users = form.save(commit=False)
        users.set_password(form.cleaned_data['password'])
        users.shop = self.request.user.shop
        users.is_staff = True
        users.save()
        # sending mail with celery
        current_site = get_current_site(self.request).domain
        activation_link = "http://" + f"{current_site}"
        credential_mail_task.delay(activation_link, form.cleaned_data['email'], form.cleaned_data['password'])
        return super().form_valid(form)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = Users
    context_object_name = 'user'
    template_name = 'users/detail.html'


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Users
    form_class = UserEditForm
    template_name = "users/update.html"
    success_url = reverse_lazy('admin_user:user_list')
    success_message = 'User updated successfully'


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = Users
    success_url = reverse_lazy('admin_user:user_list')


class UserExportView(LoginRequiredMixin, View):

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)
        writer.writerow(
            ['Id', 'First Name', 'Last Name', 'Email', 'Phone'])

        users = Users.objects.filter(shop=request.user.shop, is_staff=True, is_superuser=False)

        for user in users:
            data = [user.id, user.first_name, user.last_name, user.email, user.phone]
            writer.writerow(data)
        return response
