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
    paginate_by = 18

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        downloaded_viewed = Product.objects.order_by("-downloaded", "viewed")[:4]
        context['recomended_product'] = downloaded_viewed
        return context

class MockUpDetailView(DetailView):
    model = Product
    template_name = "detail.html"

    slug_field      = 'slug'
    slug_url_kwargs = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mockup = Product.objects.get(slug=self.kwargs['slug'])
        category = Category.objects.get(slug=mockup.category.slug)
        category_product = category.product_category.all().order_by('-downloaded', 'viewed')[:4]
        context['recomended_product'] = category_product
        return context
    
    def get_queryset(self):
        
        return super().get_queryset()
    



class MockUpListView(ListView):
    model = Product
    template_name = 'products.html'

    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        downloaded_viewed = Product.objects.order_by("-downloaded", "viewed")[:4]
        context['recomended_product'] = downloaded_viewed
        return context





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

