from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class Shop(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    branch_id = models.IntegerField()

    class Meta:
        db_table = "shop"

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if extra_fields.get('is_superuser') is True:
            user.shop = extra_fields.get('shop')
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = "users"

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('name'), max_length=30, blank=True)
    last_name = models.CharField(_('name'), max_length=30, blank=True)
    phone = models.CharField(unique=True, max_length=15, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=True, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def to_dict_json(self, index):
        return {
            'index': index,
            'pk': self.pk,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
        }
