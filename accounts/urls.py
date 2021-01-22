from django.urls import path
from .views import (
    login,
    signup,
)

app_name = "account"

urlpatterns = [
    path('login/', login, name="login"),
    path('signup/', signup, name="signup"),    
]