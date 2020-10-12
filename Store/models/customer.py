from django.db import models


class Customer(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=500)
