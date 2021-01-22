from django.shortcuts import render

# Create your views here.



def home(request, *args, **kwargs):
    template_name = "index.html"
    return render(request, template_name, {})

def aboutus(request, *args, **kwargs):
    template_name = "aboutus.html"
    return render(request, template_name, {})

def mockup(request, *args, **kwargs):
    template_name = "products.html"
    return render(request, template_name, {})

def detail(request, *args, **kwargs):
    template_name = "detail.html"
    return render(request, template_name, {})

def customer_profile(request, *args, **kwargs):
    template_name = "index.html"
    return render(request, template_name, {})

