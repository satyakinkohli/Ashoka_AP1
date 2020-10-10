from django.db import models
from .category import Category


class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    availability = models.BooleanField()
    description = models.CharField(max_length=250, default="Please buy this. The seller is broke and needs the money")
    image = models.ImageField(upload_to='upload/products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
