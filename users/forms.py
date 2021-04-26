from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from phonenumber_field.modelfields import PhoneNumberField

from .models import User



class ValidatePhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=13, required=True)

    def clean_phone_number(self):
        phonenumber = PhoneNumberField()
        try:
            phonenumber=phone_number
        except :
            raise forms.ValidationError(_("Phone number doesn't valid"))
# class RegisterForm(forms.ModelForm):
#     phone_number = forms.CharField(max_length=13, required=True)
#     password1 = forms.CharField(widget=forms.PasswordInput())
#     password2 = forms.CharField(widget=forms.PasswordInput())

#     MIN_LENGTH = 4

#     class Meta:
#         model = User
#         fields = ['phonenumber', 'password1', 'password2',]

#     def clean_username(self):
#         username = self.data.get('username')
#         return username

#     def clean_password1(self):
#         password = self.data.get('password1')
#         validate_password(password)
#         if password != self.data.get('password2'):
#             raise forms.ValidationError(_("Passwords do not match"))
#         return password

#     def clean_phonenumber(self):
#         phonenumber = self.data.get('phonenumber')
#         if User.objects.filter(phonenumber=phonenumber).exists():
#             raise forms.ValidationError(
#                 _("Another user with this phone number already exists"))
#         return phonenumber

#     def save(self, *args, **kwargs):
#         user = super(RegisterForm, self).save(*args, **kwargs)
#         user.set_password(self.cleaned_data['password1'])
#         print('Saving user with country_code', user.country_code)
#         user.save()
#         return user


# class PhoneVerificationForm(forms.Form):
#     one_time_password = forms.IntegerField()

#     class Meta:
#         fields = ['one_time_password',]



# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField()

#     class Meta:
#         fields = ['username','password']

#     def clean(self):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)
#         if not user:
#             raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
#         return self.cleaned_data

#     def login(self, request):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)
#         return user
