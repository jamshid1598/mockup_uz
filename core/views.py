from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)


from product.models import (
    Category,
    Product,
    MockUp,
    Image,
    Tag,
)
# Create your views here.



class HomeView(ListView):
    model = Product
    template_name = "index.html"
    puginate_by = 18

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context









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

