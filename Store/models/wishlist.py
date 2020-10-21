from django.db import models

from .product import Product
from .customer import Customer
from .category import Category

from django.utils import timezone


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='')
    price = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)

    def add_to_wishlist(self):
        self.save()

    @staticmethod
    def get_wishlist_by_customerid(customer_id):
        return Wishlist.objects.filter(customer=customer_id).order_by('date')

    @staticmethod
    def get_wishlist_by_productid(product_id):
        return Wishlist.objects.filter(product=product_id)

