from django.db import models
from .category import Category


class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    rating = models.PositiveSmallIntegerField(default=0)
    no_of_reviews = models.PositiveIntegerField(default=0)
    availability = models.BooleanField()
    description = models.CharField(max_length=250, default="Please buy this. The seller is broke and needs the money", null=True, blank=True)
    image = models.ImageField(upload_to='upload/products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    @staticmethod
    def get_all_product():
        return Product.objects.all()