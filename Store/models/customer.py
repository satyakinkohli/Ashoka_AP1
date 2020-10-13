from django.db import models


class Customer(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def register(self):
        self.save()

    def not_unique(self):
        if Customer.objects.filter(email=self.email):
            return True
        else:
            return False
