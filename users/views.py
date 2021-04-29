from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import json
User = get_user_model()


from random import randint
from .forms import (
	ValidatePhoneNumberForm,
	ConfirmationForm,
	PasswordCreateForm,
	LoginForm,

	PasswordResetForm,

	UserInfoForm,
)

from .models import (
	CustomToken,
	UserInfo,
)
from .session_key import current_user_session_id


def validation_phonenumber_view(request):

	session_key = current_user_session_id(request)

	template_name='registration/signup-step-1-phonenumber.html'
	
	form = ValidatePhoneNumberForm()
	if request.method=='POST':
		form = ValidatePhoneNumberForm(request.POST)
		if form.is_valid():
			phone_number = form.cleaned_data['phone_number']
			confirmation_code = randint(1000, 9999)
			print("confirmation code ", confirmation_code)
			custom_token, created = CustomToken.objects.get_or_create(phone_number=phone_number, confirmation_code=confirmation_code, session_key=session_key)
			if created:
				custom_token.delete()
				custom_token = CustomToken.objects.create(phone_number=phone_number, confirmation_code=confirmation_code, session_key=session_key)
			custom_token.save()
			messages.success(request, _("Confirmation code sent to your mobile number. The confirmation code is valid for 5 minutes."))
			return redirect('users:phone-confirmation', custom_token.key)
	return render(request, template_name, {'form': form})


def phone_verification_view(request, key):

	session_key = current_user_session_id(request)

	template_name = 'registration/signup-step-1-confirmation.html'
	try:
		custom_token = CustomToken.objects.get(key=key, session_key=session_key)
	except:
		return redirect('users:signup')
	form = ConfirmationForm()
	if request.method == 'POST':
		form = ConfirmationForm(request.POST)
		if form.is_valid():
			confirmation_code = form.cleaned_data['confirmation_code']
			if int(confirmation_code) == custom_token.confirmation_code and custom_token.check_valid_token:
				phone_number = custom_token.phone_number
				custom_token.delete()
				custom_token = CustomToken.objects.create(phone_number=phone_number, session_key=session_key)
				messages.success(request, _('Successfully confirmed, now you can create a password for your mockup.uz account'))
				return redirect('users:create-password', custom_token)
			else:
				messages.error(request, _('Password didn\'t match :(, \nOr confiramtion code expired' ))
				form = PasswordCreateForm()
	context={'phone_number': custom_token.phone_number, 'form':form}
	return render(request, template_name, context)


def create_password_for_account(request, key):

	session_key = current_user_session_id(request)

	template_name = 'registration/signup-step-1-createpassword.html'
	try:
		custom_token = CustomToken.objects.get(key=key, session_key=session_key)
	except:
		messages.error(request, _('Something went wrong, Try again'))
		return redirect('users:signup')
	form = PasswordCreateForm()
	if request.method == 'POST':
		form = PasswordCreateForm(request.POST)
		if form.is_valid():
			phone_number = form.cleaned_data['phone_number']
			password1    = form.cleaned_data['password1']
			try:
				user = User.objects.create(phone_number=phone_number, phone_number_verified=True)
				user.set_password(password1)
				user.save()
				custom_token.delete()
				login(request, user)
				return redirect('users:user-info-2nd-step', user.pk)
			except Exception as e:
				messages.error(request, _(f"Something went wrong, {e}"))
				form = PasswordCreateForm()
				context = {'form': form, 'phone_number': custom_token.phone_number}
				return render(request, template_name, context)

	context = {'form':form, 'phone_number':custom_token.phone_number}
	return render( request, template_name, context )



def login_view(request):
	template_name='registration/login.html'
	form = LoginForm()
	if request.method =='POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			phone_number = form.cleaned_data['phone_number']
			password     = form.cleaned_data['password']

			try:
				user = User.objects.get(phone_number=phone_number)
			except:
				messages.error(request, _("This phone number haven't been registred yet"))
				form=LoginForm()
				context={'form': form}
				return render(request, template_name, context)
			user = authenticate(phone_number=phone_number, password=password)
			if user:
				login(request, user)
				messages.error(request, _('Successfully loged in' ))
				return redirect('/')
			else:
				messages.warning(request, _('Phone number or password didn\'t match, please try again' ))
		else:
			messages.error(_('Phone number or password didn\'t match, please try again' ))
			# form=LoginForm()
	context={'form': form}
	return render(request, template_name, context)


@login_required
def logout_view(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("/")
	


def reset_password_view(request):

	session_key = current_user_session_id(request)

	template_name='registration/signup-step-1-phonenumber.html'
	
	form = PasswordResetForm()
	if request.method=='POST':
		form = PasswordResetForm(request.POST)
		if form.is_valid():
			phone_number = form.cleaned_data['phone_number']
			if User.objects.filter(phone_number=phone_number).exists():	
				confirmation_code = randint(1000, 9999)
				print("confirmation code ", confirmation_code)
				custom_token, created = CustomToken.objects.get_or_create(phone_number=phone_number, confirmation_code=confirmation_code, session_key=session_key)
				if created:
					custom_token.delete()
					custom_token = CustomToken.objects.create(phone_number=phone_number, confirmation_code=confirmation_code, session_key=session_key)
				custom_token.save()
				messages.success(request, _("Confirmation code sent to your mobile number. The confirmation code is valid for 5 minutes."))
				return redirect('users:reset-password-confirmation', custom_token.key)
			else:
				messages.warning(request, _("This phone number haven't been registered yet"))
	return render(request, template_name, {'form': form})


def reset_password_confirmation_view(request, key):

	session_key = current_user_session_id(request)

	template_name = 'registration/signup-step-1-confirmation.html'
	try:
		custom_token = CustomToken.objects.get(key=key, session_key=session_key)
	except:
		return redirect('users:signup')
	form = ConfirmationForm()
	if request.method == 'POST':
		form = ConfirmationForm(request.POST)
		if form.is_valid():
			confirmation_code = form.cleaned_data['confirmation_code']
			if int(confirmation_code) == custom_token.confirmation_code and custom_token.check_valid_token:
				phone_number = custom_token.phone_number
				custom_token.delete()
				custom_token = CustomToken.objects.create(phone_number=phone_number, session_key=session_key)
				messages.success(request, _('Successfully confirmed, now you can create new password'))
				return redirect('users:reset-password-change-password', custom_token)
			else:
				messages.error(request, _('Password didn\'t match :(, \nOr confiramtion code expired' ))
				form = PasswordCreateForm()
	context={'phone_number': custom_token.phone_number, 'form':form}
	return render(request, template_name, context)


def reset_password_new_password(request, key):

	session_key = current_user_session_id(request)

	template_name = 'registration/signup-step-1-createpassword.html'
	try:
		custom_token = CustomToken.objects.get(key=key, session_key=session_key)
	except:
		messages.error(request, _('Something went wrong, Try again'))
		return redirect('users:signup')
	form = PasswordCreateForm()
	if request.method == 'POST':
		form = PasswordCreateForm(request.POST)
		if form.is_valid():
			phone_number = form.cleaned_data['phone_number']
			password1    = form.cleaned_data['password1']
			try:
				user = User.objects.get(phone_number=phone_number, phone_number_verified=True)
				user.set_password(password1)
				user.save()
				custom_token.delete()
				return redirect('users:login')
			except Exception as e:
				messages.error(request, _(f"Something went wrong, {e}"))
				form = PasswordCreateForm()
				context = {'form': form, 'phone_number': custom_token.phone_number}
				return render(request, template_name, context)

	context = {'form':form, 'phone_number':custom_token.phone_number}
	return render( request, template_name, context )



@login_required
def signup_step_2_user_info(request, pk):
	template_name='registration/signup-step-2-user_info.html'
	user = User.objects.get(pk=pk)
	instance=None
	try:
		instance = UserInfo.objects.get(phone_number=user)
	except Exception as e:
		messages.error(request, _(f"Something went wrong, {e}"))
		return redirect("users:login")
	form = UserInfoForm(instance=instance)
	if request.method=='POST':
		form = UserInfoForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, _("Registration successfully completed, \nWellcom to our membership :)"))
			return redirect('users:user-profile')
		else:
			messages.error(request, _("Something went wrong, check and try again"))
	context={'form': form, 'phone_number': user.phone_number}
	return render(request, template_name, context)


from django.views.generic import UpdateView

class SignUpStep2_UserInfo(LoginRequiredMixin, UpdateView):
	model = UserInfo
	form_class = UserInfoForm
	template_name='registration/signup-step-2-user_info.html'
	success_url='users-user-profile'

	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	user = User.objects.get(pk=kwargs.get('pk'))
	# 	context["phone_number"] = user.phone_number
	# 	return context
	
	



class UserProfile(LoginRequiredMixin, View):
	template_name='myprofile.html'
	context={}
	def get(self, request, *args, **kwargs):
		user=request.user
		user_info = UserInfo.objects.get(phone_number=user)
		self.context={'object': user_info}
		return render(request, self.template_name, self.context)
	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, self.context)


# class RegisterView(SuccessMessageMixin, FormView):
#     template_name = 'registration/register.html'
#     form_class = RegisterForm
#     success_message = "One-Time password sent to your registered mobile number. The verification code is valid for 10 minutes."

#     def form_valid(self, form):
#         user = form.save()
#         username = self.request.POST['username']
#         password = self.request.POST['password1']
#         user = authenticate(username=username, password=password)
#         try:
#             response = send_verfication_code(user)
#         except Exception as e:
#             messages.add_message(self.request, messages.ERROR,
#                                 'verification code not sent. \n'
#                                 'Please re-register.')
#             return redirect('account:signup')
#         data = json.loads(response.text)

#         print(response.status_code, response.reason)
#         print(response.text)
#         print(data['success'])
#         if data['success'] == False:
#             messages.add_message(self.request, messages.ERROR,
#                             data['message'])
#             return redirect('account:signup')

#         else:
#             kwargs = {'user': user}
#             self.request.method = 'GET'
#             return PhoneVerificationView(self.request, **kwargs)


# def PhoneVerificationView(request, **kwargs):
#     template_name = 'registration/phone_confirm.html'

#     if request.method == "POST":
#         username = request.POST['username']
#         user = User.objects.get(username=username)
#         form = PhoneVerificationForm(request.POST)
#         if form.is_valid():
#             verification_code = request.POST['one_time_password']
#             response = verify_sent_code(verification_code, user)
#             print(response.text)
#             data = json.loads(response.text)

#             if data['success'] == True:
#                 login(request, user)
#                 if user.phone_number_verified is False:
#                     user.phone_number_verified = True
#                     user.save()
#                 return redirect('/dashboard')
#             else:
#                 messages.add_message(request, messages.ERROR,
#                                 data['message'])
#                 return render(request, template_name, {'user':user})
#         else:
#             context = {
#                 'user': user,
#                 'form': form,
#             }
#             return render(request, template_name, context)

#     elif request.method == "GET":
#         try:
#             user = kwargs['user']
#             return render(request, template_name, {'user': user})
#         except:
#             return HttpResponse("Not Allowed")


# class LoginView(FormView):
#     template_name = 'registration/login.html'
#     form_class = LoginForm
#     # success_url = '/dashboard'
#     success_url = '/'

#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             messages.add_message(self.request, messages.INFO,
#                                 "User already logged in")
#             return redirect('/dashboard')
#         else:
#             return super().dispatch(request, *args, **kwargs)

#     def form_valid(self, form):
#         user = form.login(self.request)
#         print(user.two_factor_auth)
#         if user.two_factor_auth is False:
#             login(self.request, user)
#             return redirect('/dashboard')
#         else:
#             try:
#                 response = send_verfication_code(user)
#                 pass
#             except Exception as e:
#                 messages.add_message(self.request, messages.ERROR,
#                                     'verification code not sent. \n'
#                                     'Please retry logging in.')
#                 return redirect('/login')
#             data = json.loads(response.text)

#             if data['success'] == False:
#                 messages.add_message(self.request, messages.ERROR,
#                                 data['message'])
#                 return redirect('/login')

#             print(response.status_code, response.reason)
#             print(response.text)
#             if data['success'] == True:
#                 self.request.method = "GET"
#                 print(self.request.method)
#                 kwargs = {'user':user}
#                 return PhoneVerificationView(self.request, **kwargs)
#             else:
#                 messages.add_message(self.request, messages.ERROR,
#                         data['message'])
#                 return redirect('/login')


# @method_decorator(login_required(login_url="/login/"), name='dispatch')
# class DashboardView(SuccessMessageMixin, View):
#     template_name = 'dashboard.html'

#     def get(self, request):
#         context = {
#             'user':self.request.user,
#             }
#         if not request.user.phone_number_verified:
#             messages.add_message(self.request, messages.INFO,
#                                 "User Not verified.")
#         return render(self.request, self.template_name, context)

#     def post(self, request):
#         if 'two_factor_auth' in request.POST:
#             if request.user.two_factor_auth:
#                 request.user.two_factor_auth = False
#             else:
#                 request.user.two_factor_auth = True
#             request.user.save()

#         return render(self.request, self.template_name, {})
