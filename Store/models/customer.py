from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=50, default='')
    email = models.EmailField()
    password = models.CharField(max_length=500)

    fname = models.CharField(max_length=50, default='')
    mobile = models.IntegerField(null=True)
    address = models.CharField(max_length=500, default='')

    def register(self):
        self.save()

    @staticmethod
    def get_customer_through_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    @staticmethod
    def get_customer_through_id(id):
        try:
            return Customer.objects.get(id=id)
        except:
            return False

    def not_unique(self):
        if Customer.objects.filter(email=self.email):
            return True
        else:
            return False
