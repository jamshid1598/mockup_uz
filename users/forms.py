from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import User #, UserInfo



class PhoneNumberForm(forms.Form):
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
		if not len(code) == 5:
			raise forms.ValidationError(_('Confirmation code must contains 5 digit'))
		return code


class SignUpForm(forms.Form):
	full_name = forms.CharField(widget=forms.TextInput(attrs={
		'class':"form-control input-lg", 'id':"id_full_name", 'name':"full_name", 'style':"width: 100%", 'type':"text", 'placeholder':'(e.x) Jhone Doe'
	}))
	phone_number = PhoneNumberField(widget=forms.TextInput(attrs={
		'class':"form-control input-lg", 'id':"id_phone_number", 'name':"phone_number", 'style':"width: 100%", 'type':"text"
	}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={
		'class':"form-control input-lg", 'id':"id_password1", 'name':"password1", 'style':"width: 100%", 'type':"password" 
	}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={
		'class':"form-control input-lg", 'id':"id_password2", 'name':"password2", 'style':"width: 100%", 'type':"password" 
	}))

	def clean_phone_number(self):
		phone_number = self.data.get('phone_number')
		if User.objects.filter(phone_number=phone_number).exists():
			raise forms.ValidationError(_('Another user with this phone number is allready exists, \nTry diffrent phone number'))
		return phone_number


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




class PasswordResetPhonenumberForm(forms.Form):
	phone_number = PhoneNumberField(widget=forms.TextInput(
		attrs={'class':"form-control input-lg", 'id':"id_phone_number", 'name':"phone_number", 'style':"width: 100%", 'type':"text", 'placeholder':"phone number"}))

	def clean_phone_number(self):
	    phone_number = self.data.get('phone_number')
	    if not User.objects.filter(phone_number=phone_number).exists():
	        raise forms.ValidationError(_('This phone number haven\'t been registered yet'))
	    return phone_number


class PasswordResetVerificationForm(forms.Form):
	confirmation_code = forms.CharField(widget=forms.NumberInput(attrs={
		'class':"form-control input-lg", 'id':"id_confirmation_code", 'name':"confirmation_code", 'style':"width: 100%", 'type':"number", 'placeholder':"4 digit confirmation code",
	}))

	def clean_confirmation_code(self):
		code = self.data.get('confirmation_code')
		if not len(code) == 5:
			raise forms.ValidationError(_('Confirmation code must contains 5 digit'))
		return code


class PasswordResetNewpasswordForm(forms.Form):
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