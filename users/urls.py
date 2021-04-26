from django.urls import path
from .views import ValidatePhoneNumberView

    # RegisterView,
    # PhoneVerificationView,
    # LoginView,
    # DashboardView,


app_name = "users"

urlpatterns = [
    path('phone-number/', ValidatePhoneNumberView.as_view(), name='phone-number')
    # path('login/', LoginView.as_view(), name="login"),
    # path('signup/', RegisterView.as_view(), name="signup"),
    # path('dashboard/', DashboardView.as_view(), name="dashboard"),    
]