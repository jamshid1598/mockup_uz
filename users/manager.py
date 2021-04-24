from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):

  def _create_user(self, phonenumber, email, password, is_staff, is_superuser, **extra_fields):
    if not phonenumber:
        raise ValueError('Users must have an phone number')
    
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        phonenumber=phonenumber,
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self,phonenumber, email, password, **extra_fields):
    return self._create_user(phonenumber, email, password, False, False, **extra_fields)

  def create_superuser(self, phonenumber, email, password, **extra_fields):
    user=self._create_user(phonenumber, email, password, True, True, **extra_fields)
    user.save(using=self._db)
    return user