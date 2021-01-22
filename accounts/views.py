from django.shortcuts import render

# Create your views here.
def login(request, *args, **kwargs):
    template_name = "registration/login.html"
    return render(request, template_name, {})

def signup(request, *args, **kwargs):
    template_name = "registration/register.html"
    return render(request, template_name, {})