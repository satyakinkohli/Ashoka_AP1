from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password 


# Create your views here.

from django.http import HttpResponse

from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.views import View


def home(request):
    return render(request, 'FrontEnd/try6.html')


def index(request):
    categories = Category.get_all_categories()

    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_product_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()

    data = {'products': products, 'categories': categories}

    return render(request, 'index.html', data)

class Signup(View):
    def get(self,request):
        return render(request, 'signup.html')

    def post(self,request):
        data_posted = request.POST
        email = data_posted.get('email')
        password = data_posted.get('password')

        saved_value = {
            'email': email
        }

        error = None

        customer = Customer(email=email, password=password)

        if len(password) < 6:
            error = "Password must be at least 6 characters long."
        elif customer.not_unique():
            error = "This email address already has another account linked with it."

        if not error:
            # customer.password = make_password('customer.password')
            customer.register()
            return redirect("Nostalgia_Menu")
        else:
            data = {'error': error, 'saved_value': saved_value}
            return render(request, 'signup.html', data)




class Login(View):
    def get(self,request):
        return render(request, 'login.html')


    def post(Self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_through_email(email)
        error_message = None
        if customer:
            # result = check_password(password, customer.password)
            if password == customer.password:
            # if result:
                return redirect("Nostalgia_Menu")
            else:
                error_message = "Incorrect email or password"
        else:
            error_message = "Incorrect email or password"

        return render(request, 'login.html', {'error': error_message})


        
