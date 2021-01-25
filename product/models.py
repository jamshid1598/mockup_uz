from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from  django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=250)

    image = models.ImageField(upload_to="category-image/%d/%m/%Y/")
    caption = models.CharField(max_length=300)

    def __str__(self):
        return self.name
    


class Tag(models.Model):
    category = models.ManyToManyField(Category)
    tag = models.CharField(max_length=50)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=300)
    description = models.TextField()
    price = models.FloatField(blank=True, null=True, validators=(MinValueValidator(0), MaxValueValidator(100000000)))
    discount = models.FloatField(blank=True, null=True, validators=(MinValueValidator(0), MaxValueValidator(100000000)))
    paid = models.BooleanField(default=True)
    free = models.BooleanField(default=False) 

    downloaded = models.SmallIntegerField(default=0)
    viewed = models.SmallIntegerField(default=0)

    liked = models.ManyToManyField(User)
    tags = models.ManyToManyField(Tag)

    def __str_(self):
        return self.name + " | " + self.category.name

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    
    image = models.ImageField(upload_to="product-image/%d/%m/%Y/")
    caption = models.CharField(max_length=300)

    def __str__(self):
        return "image pk: "+(self.pk)+self.product.name

class MockUp(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_file")

    file = models.FileField(upload_to="mockup-file/%d/%m/%Y/")
    resolution = models.CharField(max_length=50)
    extension = models.CharField(max_length=10)
    size = models.CharField(max_length=10)

