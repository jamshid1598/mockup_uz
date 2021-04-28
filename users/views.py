from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
import json
from random import randint
from .forms import (
	ValidatePhoneNumberForm,
	ConfirmationForm,
	PasswordCreateForm,
	LoginForm,
) # RegisterForm, LoginForm, PhoneVerificationForm
# from .authy_api import send_verfication_code, verify_sent_code
# from .models import User

from .models import (
	CustomToken,
)



# class ValidatePhoneNumberView(SuccessMessageMixin, FormView):
#     template_name = 'registration/signup-step-1-phonenumber.html'
#     form_class = ValidatePhoneNumberForm
#     success_message = _("Confirmation code sent to your registered mobile number. The confirmation code is valid for 10 minutes.")

	# def get_success_url(self):
	#     return reverse('users:phone-confirmation')


def validation_phonenumber_view(request):

	if not request.session.exists(request.session.session_key):
		request.session.create() 
	session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)

	template_name='registration/signup-step-1-phonenumber.html'

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
			messages.success(request, _("Confirmation code sent to your registered mobile number. The confirmation code is valid for 5 minutes."))
			return redirect('users:phone-confirmation', custom_token.key)
		else:
			return render(request, template_name, {'form': form})
	else:
		form = ValidatePhoneNumberForm()
	return render(request, template_name, {'form': form})


def phone_verification_view(request, key):

	if not request.session.exists(request.session.session_key):
		request.session.create() 
	session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)

	template_name = 'registration/signup-step-1-confirmation.html'
	try:
		custom_token = CustomToken.objects.get(key=key, session_key=session_key)
		created_at   = custom_token.created

		print("time: ", created_at.strftime("%Y-%m-%d %H:%M:%S"), timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
	except:
		return redirect('users:phone-number')
	form = ConfirmationForm(request.POST)
	if form.is_valid():
		confirmation_code = form.cleaned_data['confirmation_code']
		confirmation_code = int(confirmation_code)
		if confirmation_code == custom_token.confirmation_code:
			phone_number = custom_token.phone_number
			custom_token.delete()
			custom_token = CustomToken.objects.create(phone_number=phone_number, session_key=session_key)
			messages.success(request, _('Successfully confirmed, now you can create a password for your mockup.uz account'))
			return redirect('users:create-password', custom_token)
		else:
			messages.error(request, _('Password didn\'t match :(, \nTry again'))
	print('session', request.session.session_key)
	context={'phone_number': custom_token.phone_number, 'form':form}
	return render(request, template_name, context)


def create_password_for_account(request, key):

	if not request.session.exists(request.session.session_key):
		request.session.create() 
	session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)

	template_name = 'registration/signup-step-1-createpassword.html'
	try:
		custom_token = CustomToken.objects.get(key=key, session_key=session_key)
	except:
		messages.error(request, _('Something went wrong, Try again'))
		return redirect('users:phone-number')

	form = PasswordCreateForm(request.POST)
	if form.is_valid():
		phone_number = form.cleaned_data['phone_number']
		password1    = form.cleaned_data['password1']
		user = User.objects.create(phone_number=phone_number, phone_number_verified=True)
		user.set_password(password1)
		user.save()
		login(request, user)
		return redirect('/')
	else:
		# messages.error(request, _('Something went wrong, plz check and try again'))
		form = PasswordCreateForm()
	context = {'form':form, 'phone_number':custom_token.phone_number}

	return render(
		request,
		template_name,
		context
	)


def login_view(request):
	template_name='registration/login.html'
	if request.method =='POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			phone_number = form.cleaned_data['phone_number']
			password     = form.cleaned_data['password']

			user = authenticate(phone_number=phone_number, password=password)
			if user:
				login(request, user)
				messages.error(request, _('Successfully loged in' ))
				return redirect('/')
			else:
				messages.error(_('Phone number or password didn\'t match, please try again' ))
		else:
			messages.error(_('Phone number or password didn\'t match, please try again' ))
			form=LoginForm()
			context={'form': form}
			return render(request, template_name, context)
	else:
		form=LoginForm()
	context={'form': form}
	return render(request, template_name, context)




@login_required
def logout_view(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("/")
	


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
