from django.urls import path
from .views import (
    HomeView,
    MockUpDetailView,
    MockUpListView,

    download_counter,

    aboutus,
    UseFullListView,
)
app_name = "core"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('home/<slug:slug>/', HomeView.as_view(), name="home"),
    path("detail/<slug:slug>/", MockUpDetailView.as_view(), name="detail"),
    
    path("mockups/", MockUpListView.as_view(), name="mockup"),
    path("mockups/<slug:slug>/", MockUpListView.as_view(), name="mockup"),

    path('ajax/download_counter/', download_counter, name='download_counter'),

    path("about-us/", aboutus, name="aboutus"),
    path("usefull-page/", UseFullListView.as_view(), name="usefull"),    
]