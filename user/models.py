from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from . import managers


class User(AbstractBaseUser, PermissionsMixin):
    USER_CHOICES = (
    ('Admin', 'Admin'),
    ('Customer', 'Customer'),
    )
    email = models.EmailField(_('Email Address'), unique=True)
    username = models.CharField(_('Username'), max_length=30, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True,blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    user_type=models.CharField(max_length=10, choices=USER_CHOICES,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(_('Active'), default=False)
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    objects = managers.UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.username
