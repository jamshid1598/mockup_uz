from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import User, UserInfo



class ValidatePhoneNumberForm(forms.Form):
	phone_number = PhoneNumberField(widget=forms.TextInput(
		attrs={'class':"form-control input-lg", 'id':"id_phone_number", 'name':"phone_number", 'style':"width: 100%", 'type':"text", 'placeholder':"phone number"}))

	def clean_phone_number(self):
		phone_number = self.data.get('phone_number')
		if User.objects.filter(phone_number=phone_number).exists():
			raise forms.ValidationError(_('Another user with this phone number is allready exists, \nTry diffrent phone number'))
		return phone_number

class ConfirmationForm(forms.Form):
	confirmation_code = forms.CharField(widget=forms.NumberInput(attrs={
		'class':"form-control input-lg", 'id':"id_confirmation_code", 'name':"confirmation_code", 'style':"width: 100%", 'type':"number", 'placeholder':"4 digit confirmation code",
	}))

	def clean_confirmation_code(self):
		code = self.data.get('confirmation_code')
		if not len(code) == 4:
			# print("Code", type(code))
			raise forms.ValidationError(_('Confirmation code must contains 4 digit'))
		return code

class PasswordCreateForm(forms.Form):
	phone_number = PhoneNumberField(widget=forms.TextInput(attrs={
		'class':"form-control input-lg", 'id':"id_phone_number", 'name':"phone_number", 'style':"width: 100%", 'type':"hidden"
	}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={
		'class':"form-control input-lg", 'id':"id_password1", 'name':"password1", 'style':"width: 100%", 'type':"password" 
	}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={
		'class':"form-control input-lg", 'id':"id_password2", 'name':"password2", 'style':"width: 100%", 'type':"password" 
	}))

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


class PasswordResetForm(forms.Form):
	phone_number = PhoneNumberField(widget=forms.TextInput(
		attrs={'class':"form-control input-lg", 'id':"id_phone_number", 'name':"phone_number", 'style':"width: 100%", 'type':"text", 'placeholder':"phone number"}))

	# def clean_phone_number(self):
	#     phone_number = self.data.get('phone_number')
	#     if not User.objects.filter(phone_number=phone_number).exists():
	#         raise forms.ValidationError(_('This phone number haven\'t been registered yet'))
	#     return phone_number


class UserInfoForm(forms.ModelForm):  
	image            = forms.ImageField(widget=forms.FileInput(attrs={
		'class':"form-control input-lg", 'id':"id_image", 'name':"image", 'style':"width: 100%", 'type':"file"
	}))      
	full_name        = forms.CharField( widget=forms.TextInput(attrs={
		'class':"form-control input-lg", 'id':"id_full_name", 'name':"full_name", 'style':"width: 100%", 'type':"text", 'placeholder':"(e.x) John Don"
	}))
	email            = forms.EmailField(widget=forms.EmailInput(attrs={
		'class':"form-control input-lg", 'id':"id_email", 'name':"email", 'style':"width: 100%", 'type':"email", 'placeholder':"(e.x) example@gmail.com"
	}))
	address          = forms.CharField(widget=forms.TextInput(attrs={
		'class':"form-control input-lg", 'id':"id_address", 'name':"address", 'style':"width: 100%", 'type':"text", 'placeholder': '(e.x) 01, Mirzo Ulug\'bek district, Tashkent City'
	}))
	company          = forms.CharField(widget=forms.TextInput(attrs={
		'class':"form-control input-lg", 'id':"id_company", 'name':"company", 'style':"width: 100%", 'type':"text", 'placeholder': '(e.x) Marvel Creative'
	}))
	company_web_site = forms.CharField(widget=forms.TextInput(attrs={
		'class':"form-control input-lg", 'id':"id_company_web_site", 'name':"company_web_site", 'style':"width: 100%", 'type':"text", 'placeholder':"(e.x) https://myprint.uz"
	}))
	company_address  = forms.CharField(widget=forms.TextInput(attrs={
		'class':"form-control input-lg", 'id':"id_company_address", 'name':"company_address", 'style':"width: 100%", 'type':"text", 'placeholder':"(e.x) 32A, Chilonzor 14, Tashkent city"
	}))
	 
	class Meta:
		model = UserInfo
		fields = ['image', 'full_name', 'email', 'address', 'company', 'company_web_site', 'company_address', ]


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
