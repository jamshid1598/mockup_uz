from django.contrib import admin
from django.db.models import TextField
from tinymce.widgets import TinyMCE
from .models import (
    Category,
    Product,
    MockUp,
    Image,
    Tag,

)
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    #  ('name', 'slug', 'image', 'caption', )
    list_display  = ('name',)
    orderinig     = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)

    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Category', {
            "fields": (
                'name', 'slug', 'image', 'caption'
            ),
        }),
    )

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    # ('category', 'name', 'slug', 'description', 'price', 'discount', 'paid', 'free', 'downloaded', 'viewed', 'liked', 'tags', )
    list_display = ('category', 'name', 'price', 'discount', 'paid', 'free', 'downloaded', 'viewed',)
    list_display_links = ('name', 'downloaded', 'viewed')
    ordering = ('category', 'name', 'price', 'discount', 'paid', 'free', 'downloaded', 'viewed', 'tags')
    search_fields = ('category', 'name', 'price', 'discount', 'paid', 'free', 'downloaded', 'viewed', 'tags')

    list_editable = ('category', 'price', 'discount', 'paid', 'free', )

    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Category', {
            "fields": (
                'category',
            ),
        }),
        ('MockUp Info', {
            "fields": (
                'name', 'slug', 'description', 'tags',
            )
        }),
        ('Price Info', {
            'fields' : (
                'price', 'discount', 'paid', 'free',
            )
        }),
    )

    formfield_overrides = {
        TextField: {'widget': TinyMCE }
    }    


admin.site.register(Product, ProductAdmin)