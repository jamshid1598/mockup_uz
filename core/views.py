from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import  JsonResponse
from django.db.models import F, Q, When, Value, Case
from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	CreateView,
	DeleteView,
)
import json

from product.models import (
	UserViews,
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
		downloaded_viewed = Product.objects.order_by("-downloaded",)[:4]
		context['recomended_product'] = downloaded_viewed
		return context



class MockUpDetailView(DetailView):
	model = Product
	template_name = "detail.html"

	slug_field      = 'slug'
	slug_url_kwargs = 'slug'
	
	def get_client_ip(self, request, *args, **kwargs):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		print(ip)
		return ip

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		mockup = Product.objects.get(slug=self.kwargs['slug'])

		# Product.objects.filter(slug=self.kwargs['slug']).update(viewed=F('viewed')+1) # increase viewed field by 1 every request, count viewed 
		# <--------- view counter by ip ---------!>
		visitor_ip = self.get_client_ip(self.request)
		print(visitor_ip)
		UserViews.objects.get_or_create(visitor_ip=visitor_ip, mockup=mockup)
		# <--------- view counter by ip ---------!>

		category = Category.objects.get(slug=mockup.category.slug)
		category_product = category.product_category.all().order_by('-downloaded',)[:4]
		context['recomended_product'] = category_product
		return context



class MockUpListView(ListView):
	model = Product
	template_name = 'products.html'
	paginate_by = 9

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		downloaded_viewed = Product.objects.order_by("-downloaded",)[:4]
		context['recomended_product'] = downloaded_viewed
		return context

	def get_queryset(self):
		try:
			slug = self.kwargs['slug']
			category = get_object_or_404(Category, slug=slug)
			return category.product_category.all()
		except:
			return Product.objects.all()


def download_counter(request):
	data = json.loads(request.body)
	slug = data['slug']
	Product.objects.filter(slug = slug).update(downloaded = F('downloaded')+1)
	return JsonResponse({"success":"Increased"}, safe=False, status=200)


def aboutus(request, *args, **kwargs):
	template_name = "aboutus.html"
	return render(request, template_name, {})

def customer_profile(request, *args, **kwargs):
	template_name = "index.html"
	return render(request, template_name, {})

