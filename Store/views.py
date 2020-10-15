from django.shortcuts import render, redirect
# from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

from django.http import HttpResponse

from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.views import View


def home(request):
    return render(request, 'FrontEnd/try6.html')


class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {product: 1}

        request.session['cart'] = cart
        return redirect('Nostalgia_Menu')

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}

        products = None
        categories = Category.get_all_categories()

        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_product_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()

        data = {'products': products, 'categories': categories}

        return render(request, 'index.html', data)


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
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
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_through_email(email)
        error_message = None
        if customer:
            # result = check_password(password, customer.password)
            # if result:
            if password == customer.password:
                request.session['customer'] = customer.id
                
                return redirect("Nostalgia_Menu")
            else:
                error_message = "Incorrect email or password"
        else:
            error_message = "Incorrect email or password"

        return render(request, 'login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('/')


class Cart(View):
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
            return render(request, 'cart.html')
        else:
            ids = list(request.session.get('cart').keys())
            products = Product.get_all_product_by_id(ids)
            return render(request, 'cart.html', {'products': products})


def checkout(request):
    # URGENT: add to orders
    request.session['cart'] = {}
    return render(request, 'checkout.html')
