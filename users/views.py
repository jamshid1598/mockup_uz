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
import json
from .forms import (
    ValidatePhoneNumberForm,
) # RegisterForm, LoginForm, PhoneVerificationForm
# from .authy_api import send_verfication_code, verify_sent_code
# from .models import User




class ValidatePhoneNumberView(SuccessMessageMixin, FormView):
    template_name = 'registration/signup-step-1-phonenumber.html'
    form_class = ValidatePhoneNumberForm
    success_message = _("Confirmation code sent to your registered mobile number. The confirmation code is valid for 10 minutes.")

    def get_success_url(self):
        return reverse('users:phone-confirmation')

def validation_phonenumber_view(self, request):
    template_name='registration/signup-step-1-phonenumber.html'
    form =ValidatePhoneNumberForm()



def phone_verification_view(request):
    template_name = 'registration/signup-step-1-confirmation.html'
    context={}
    return render(request, template_name, context)


# def logout(request):
#     request.logout()


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
