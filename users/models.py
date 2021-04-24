from datetime import date
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phonenumber = PhoneNumberField(_('phonenumber'), unique=True)
    email = models.EmailField(_('email'), max_length=254, blank=True, null=True, unique=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_superuser = models.BooleanField(_('is_superuser'), default=False)
    is_active = models.BooleanField(_('is_active'), default=True)
    last_login = models.DateTimeField(_('last_login'), null=True, blank=True)
    date_joined = models.DateTimeField(_("date_joined"), auto_now_add=True)
    phone_number_verified = models.BooleanField(default=False)
    change_pw = models.BooleanField(default=True)


    objects = UserManager()

    USERNAME_FIELD = 'phonenumber'
    PHONENUMBER_FIELD = 'phonenumber'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email',]

    class Meta:
        ordering = ('phonenumber', 'email')
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return str(self.phonenumber)

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

