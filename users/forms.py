from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import User



class ValidatePhoneNumberForm(forms.Form):
    phone_number = PhoneNumberField(widget=forms.TextInput(
        attrs={'class':"form-control input-lg", 'id':"id_phone_number", 'name':"phone_number", 'style':"width: 100%", 'type':"text", 'placeholder':"phone number"}))

    def clean_phone_number(self):
        phone_number = self.data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(_('Another user with this phone number is allready exists, \nTry diffrent phone number'))
        return phone_number

        
class ConfirmationForm(forms.Form):
    confirmation_code = forms.CharField(max_length=4, widget=forms.NumberInput(attrs={
        'class':"form-control input-lg", 'id':"id_confirmation_code", 'name':"confirmation_code", 'style':"width: 100%", 'type':"number", 'placeholder':"4 digit confirmation code",
    }))

    def clean_confirmation_code(self):
        code = self.data.get('confirmation_code')
        if len(code) > 4 or len(code) < 4:
            raise forms.ValidationError(_('Confirmation code didn\'t match'))
        return code


class PasswordCreateForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':"form-control input-lg", 'id':"id_password1", 'name':"password1", 'style':"width: 100%", 'type':"password" 
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':"form-control input-lg", 'id':"id_password2", 'name':"password2", 'style':"width: 100%", 'type':"password" 
    }))
    class Meta:
        model = User
        fields = ['phone_number', 'password1', 'password2']

    def clean_password1(self):
        password1 = self.data.get('password1')
        password2 = self.data.get('password2')
        if password1 != password2:
            raise forms.ValidationError(_('Passwords didn\'t match, \nPlease check and try again'))
        elif len(password1) < 8:
            raise forms.ValidationError(_("Password must contains at least 8 charachter"))
        return password1

class LoginForm(forms.Form):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={
        'class':"form-control input-lg", 'id':"id_phone_number", 'name':"phone_number", 'style':"width: 100%", 'type':"text", 'placeholder':"phone number"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':"form-control input-lg", 'id':"id_password", 'name':"password", 'style':"width: 100%", 'type':"password" 
    }))



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
