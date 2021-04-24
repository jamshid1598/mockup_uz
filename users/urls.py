from django.urls import path
from .views import (
    RegisterView,
    PhoneVerificationView,
    LoginView,
    DashboardView,

)

app_name = "account"

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('signup/', RegisterView.as_view(), name="signup"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),    
]