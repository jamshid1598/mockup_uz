from django.urls import path
from .views import (
    home,
    mockup,
    detail,
    aboutus,
)
app_name = "core"

urlpatterns = [
    path('', home, name="home"),
    path("mockups-collect/", mockup, name="mockup"),
    path("detail/", detail, name="detail"),
    path("about-us/", aboutus, name="aboutus"),    
]