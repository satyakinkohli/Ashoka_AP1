from django.db import models
from django.db.models import Q

from .category import Category


class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    no_of_reviews = models.PositiveIntegerField(default=0)
    availability = models.BooleanField()
    description = models.CharField(max_length=250, default="Please buy this. The seller is broke and needs the money", null=True, blank=True)
    image = models.ImageField(upload_to='upload/products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    @staticmethod
    def get_all_product_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_product_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

