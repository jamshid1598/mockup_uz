from django.urls import path
from .views import (
    ValidatePhoneNumberView, 
    phone_verification_view,
    logout,
)

    # RegisterView,
    # PhoneVerificationView,
    # LoginView,
    # DashboardView,


app_name = "users"

urlpatterns = [
    path('phone-number/', ValidatePhoneNumberView.as_view(), name='phone-number'),
    path('phone/confirmation/', phone_verification_view, name='phone-confirmation'),
    path('logout/', logout, name="logout"),
    # path('signup/', RegisterView.as_view(), name="signup"),
    # path('dashboard/', DashboardView.as_view(), name="dashboard"),    
]