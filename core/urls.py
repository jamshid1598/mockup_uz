from django.urls import path
from .views import (
    HomeView,
    MockUpDetailView,


    home,
    mockup,
    detail,
    aboutus,
)
app_name = "core"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path("detail/<slug:slug>/", MockUpDetailView.as_view(), name="detail"),
        path("mockups-collect/", mockup, name="mockup"),
    path("about-us/", aboutus, name="aboutus"),    
]