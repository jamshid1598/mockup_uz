from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):

  def _create_user(self, phone_number, password1, is_staff, is_superuser, **extra_fields):
    if not phone_number:
        raise ValueError('Users must have an phone number')
    
    now = timezone.now()
    # email = self.normalize_email(email)
    user = self.model(
        phone_number=phone_number,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password1)
    user.save(using=self._db)
    return user

  def create_user(self,phone_number, password1, **extra_fields):
    return self._create_user(phone_number, password1, False, False, **extra_fields)

  def create_superuser(self, phone_number, password1, **extra_fields):
    user=self._create_user(phone_number, password1, True, True, **extra_fields)
    user.save(using=self._db)
    return user



    