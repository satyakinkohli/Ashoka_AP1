from django.db import models


class Customer(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def register(self):
        self.save()



    @staticmethod
    def get_customer_through_email(email):
    	try:
    		return Customer.objects.get(email=email)
    	except:
    		return False


    def not_unique(self):
        if Customer.objects.filter(email=self.email):
            return True
        else:
            return False
