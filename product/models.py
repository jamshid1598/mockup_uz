from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from  django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    slug = models.SlugField(max_length=250, verbose_name="Slug")

    image = models.ImageField(upload_to="category-image/%d/%m/%Y/", blank=True, null=True, verbose_name="Image")
    caption = models.CharField(max_length=300, blank=True, null=True, verbose_name="Caption")

    def __str__(self):
        return self.name
    


class Tag(models.Model):
    category = models.ManyToManyField(Category, verbose_name="Category")
    tag = models.CharField(max_length=50, verbose_name="Tag Name")


class Product(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name='product_category', verbose_name="Category")

    name = models.CharField(max_length=200, verbose_name="Name")
    slug = models.SlugField(max_length=300, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    price = models.FloatField(blank=True, null=True, validators=(MinValueValidator(0), MaxValueValidator(100000000)), verbose_name="Price")
    discount = models.FloatField(blank=True, null=True, validators=(MinValueValidator(0), MaxValueValidator(100000000)), verbose_name="Discount")
    paid = models.BooleanField(default=True, verbose_name="Paid")
    free = models.BooleanField(default=False, verbose_name="Free") 

    downloaded = models.SmallIntegerField(default=0)
    viewed = models.SmallIntegerField(default=0)

    liked = models.ManyToManyField(User, related_name="user_likes",)
    tags = models.ManyToManyField(Tag, related_name="product_tags", verbose_name="Product Tags")

    def __str_(self):
        return self.name + " | " + self.category.name

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image", verbose_name="Product")
    
    image = models.ImageField(upload_to="product-image/%d/%m/%Y/", verbose_name="Image")
    caption = models.CharField(max_length=300, blank=True, null=True, verbose_name="Caption")

    def __str__(self):
        return "image pk: "+(self.pk)+self.product.name

class MockUp(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_file", verbose_name="Product")

    file = models.FileField(upload_to="mockup-file/%d/%m/%Y/", verbose_name="MockUp File")
    resolution = models.CharField(max_length=50, blank=True, null=True, verbose_name="Resolution")
    extension = models.CharField(max_length=10, blank=True, null=True, verbose_name="Extension")
    size = models.CharField(max_length=10, blank=True, null=True, verbose_name="Size")

    def __str__(self):
        return "File pk: "+str(self.pk)+self.product.name
