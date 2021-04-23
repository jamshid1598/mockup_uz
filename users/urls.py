from django.urls import path
from .views import *
from allauth.account.forms import LoginForm
from allauth.account.views import LoginView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
]