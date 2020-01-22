from django.db import models
from pyuploadcare.dj.models import ImageField
from django.conf import settings

# Create your models here.

class Category(models.Model):
    categoryy = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.categoryy

    def save_category(self):
        self.save()

    def delete_category(self):
        self.delete()


class Product(models.Model):
    prod_pic = ImageField(manual_crop='', blank=True)
    title = models.CharField(max_length=100)
    price = models.FloatField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


    @classmethod
    def search_category(cls,search_term):
        category = cls.objects.filter(category__categ__icontains=search_term)

        return category

class OrderedProduct(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    ordered = models.BooleanField(default=False)
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    product = models.ManyToManyField(OrderedProduct)
    ordered = models.BooleanField(default=False)
    posted = models.DateTimeField(auto_now_add=True, null=True)
   

