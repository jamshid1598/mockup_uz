from django.urls import path
from .views import (
    login_view,
    # ValidatePhoneNumberView, 
    validation_phonenumber_view,
    phone_verification_view,
    create_password_for_account,
    logout_view,
)

    # RegisterView,
    # PhoneVerificationView,
    # LoginView,
    # DashboardView,


app_name = "users"

urlpatterns = [
    path('login/', login_view, name='login'),

    path('phone/number/', validation_phonenumber_view, name='phone-number'),
    path('phone/confirmation/<str:key>/', phone_verification_view, name='phone-confirmation'),
    path('create/password/<str:key>/', create_password_for_account, name='create-password'),
    path('logout/', logout_view, name="logout"),
    # path('signup/', RegisterView.as_view(), name="signup"),
    # path('dashboard/', DashboardView.as_view(), name="dashboard"),    
]