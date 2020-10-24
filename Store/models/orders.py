from django.db import models

from .product import Product
from .customer import Customer
from .category import Category

from django.utils import timezone


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='')
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.PositiveIntegerField()
    rating = models.PositiveSmallIntegerField(default=5)
    date = models.DateTimeField(default=timezone.now)

    def place_order(self):
        self.save()

    @staticmethod
    def get_orders_by_customerid(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('date')

    @staticmethod
    def get_orders_by_orderid(product_id):
        return Order.objects.filter(product=product_id)
