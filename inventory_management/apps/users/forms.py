from django import forms
from django.contrib.auth import password_validation

from .models import Users


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label='Enter First Name', min_length=4, max_length=50, widget=forms.TextInput)
    last_name = forms.CharField(label='Enter Last Name', min_length=4, max_length=50, widget=forms.TextInput)
    email = forms.EmailField(max_length=100, error_messages={'required': 'Sorry, you will need an email'},
                             widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ('email', 'first_name', 'last_name', 'phone')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')

        user = Users(first_name=cd.get('first_name'), last_name=cd.get('last_name'), phone=cd.get('phone'),
                     email=cd.get('email'))
        password_validation.validate_password(cd['password2'], user)
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, this is already taken')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone = phone[1:4] + phone[6:9] + phone[10:]
        if len(str(phone)) != 10:
            raise forms.ValidationError(
                'Please use valid Phone')
        if Users.objects.filter(phone=phone).exists():
            raise forms.ValidationError(
                'Please use another Phone, this is already taken')
        return phone


class PwdResetForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = Users.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunately we can not find this email address')
        return email


class PwdResetConfirmForm(forms.Form):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))

    def clean_new_password2(self):
        cd = self.cleaned_data
        if cd['new_password1'] != cd['new_password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['new_password2']


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        error_messages={'unique': "Please use another Email, this is already taken"},
        label='Account email', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email'}))

    first_name = forms.CharField(
        label='First Name', min_length=4, max_length=50, widget=forms.TextInput)
    last_name = forms.CharField(
        label='Last Name', min_length=4, max_length=50, widget=forms.TextInput)

    class Meta:
        model = Users
        fields = ('email', 'first_name', 'last_name', 'phone')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone = phone[1:4] + phone[6:9] + phone[10:]
        if len(str(phone)) != 10:
            raise forms.ValidationError(
                'Please use valid Phone')
        return phone
