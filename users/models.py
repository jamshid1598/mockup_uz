from datetime import date
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number          = PhoneNumberField(_('phone_number'), unique=True)
    is_staff              = models.BooleanField(_('is_staff'), default=False)
    is_superuser          = models.BooleanField(_('is_superuser'), default=False)
    is_active             = models.BooleanField(_('is_active'), default=True)
    last_login            = models.DateTimeField(_('last_login'), null=True, blank=True)
    date_joined           = models.DateTimeField(_("date_joined"), auto_now_add=True)
    phone_number_verified = models.BooleanField(default=False)
    change_pw             = models.BooleanField(default=True)


    objects = UserManager()

    USERNAME_FIELD     = 'phone_number'
    PHONE_NUMBER_FIELD = 'phone_number'

    class Meta:
        ordering            = ('phone_number',)
        verbose_name        = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return str(self.phone_number)

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)



class UserInfo(models.Model):
    image     = models.ImageField(_('image'), upload_to='user-image/', blank=True, null=True)
    full_name = models.CharField(_('full_name'), max_length=255,)
    phone_number = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_info')
    email   = models.EmailField(_('email'), blank=True, null=True)
    address = models.CharField(_('address'), max_length=255, blank=True, null=True)
    company = models.CharField(_('company'), max_length=255, blank=True, null=True)
    company_web_site = models.URLField(_('company_web_site'), blank=True, null=True)
    company_address  = models.CharField(_('company_address'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name        = 'User\'s Info'
        verbose_name_plural = 'Users\' Info'

    def __str__(self):
        return self.full_name + " | " + str(self.phone_number.phone_number)




import binascii
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import datetime
# from my_project.companies.models import Company


class CustomToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    phone_number = PhoneNumberField(_('Phone Number'))
    confirmation_code = models.SmallIntegerField(_('Confirmation Code'), blank=True, null=True)
    session_key = models.CharField(_("Session Key"), max_length=200, blank=True, null=True)

    created = models.DateTimeField(_("Created"), default=timezone.now)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(CustomToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
    
    @property
    def check_valid_token(self):
        if self.created < datetime.datetime.now()-datetime.timedelta(minutes=5):
            e = CustomToken.objects.get(pk=self.pk)
            e.delete()
            return True
        else:
            return False