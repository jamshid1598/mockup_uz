from django.urls import path
from .views import (
    HomeView,
    MockUpDetailView,
    MockUpListView,

    mockup,
    aboutus,
)
app_name = "core"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path("detail/<slug:slug>/", MockUpDetailView.as_view(), name="detail"),
    
    path("mockups-collect/", MockUpListView.as_view(), name="mockup"),
    path("mockups-collect/<slug:slug>", MockUpListView.as_view(), name="mockup"),

    path("about-us/", aboutus, name="aboutus"),    
]