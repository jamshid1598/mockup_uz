from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),

    path('', include('core.urls', namespace="core")),
    path('product/', include('product.urls', namespace="product")),
    path('accounts/', include('users.urls', namespace='users')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)