from django.urls import path
from .views import (
    UserProfile,

    login_view,
    # ValidatePhoneNumberView, 
    validation_phonenumber_view,
    phone_verification_view,
    create_password_for_account,
    logout_view,

    reset_password_view,
    reset_password_confirmation_view,
    reset_password_new_password,
)

    # RegisterView,
    # PhoneVerificationView,
    # LoginView,
    # DashboardView,


app_name = "users"

urlpatterns = [
    path('profile/', UserProfile.as_view(), name='user-profile'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name="logout"),

    path('phone/number/', validation_phonenumber_view, name='signup'),
    path('phone/confirmation/<str:key>/', phone_verification_view, name='phone-confirmation'),
    path('create/password/<str:key>/', create_password_for_account, name='create-password'),

    path('reset/account/password/', reset_password_view, name="reset-password"),
    path('reset/account/password/confirmation/<str:key>/', reset_password_confirmation_view, name="reset-password-confirmation"),  
    path('reset/password/change_password/<str:key>/', reset_password_new_password, name='reset-password-change-password'),
]