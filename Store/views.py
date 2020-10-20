from django.shortcuts import render, redirect , HttpResponseRedirect
# from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

from django.http import HttpResponse

from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from .models.wishlist import Wishlist
from django.views import View
from Store.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator


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
        name = data_posted.get('name')
        email = data_posted.get('email')
        password = data_posted.get('password')

        saved_value = {
            'email': email,
            'name': name
        }

        error = None

        customer = Customer(name=name, email=email, password=password)

        if len(password) < 6:
            error = "Password must be at least 6 characters long."
        elif customer.not_unique():
            error = "This email address already has another account linked with it."

        if not error:
            # customer.password = make_password('customer.password')
            customer.register()
            request.session['customer'] = customer.id
            request.session['name'] = customer.name
            return redirect("Nostalgia_Menu")
        else:
            data = {'error': error, 'saved_value': saved_value}
            return render(request, 'signup.html', data)


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
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
                request.session['name'] = customer.name

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
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


@auth_middleware
def checkout(request):
    customer = request.session.get('customer')
    cart = request.session.get('cart')
    products = Product.get_all_product_by_id(list(cart.keys()))

    for product in products:
        order = Order(customer=Customer(id=customer),
                      product=product,
                      price=product.price,
                      category=product.category,
                      quantity=cart.get(str(product.id)))

        order.place_order()

    request.session['cart'] = {}

    return render(request, 'checkout.html')


class Order_View(View):
    @method_decorator(auth_middleware)
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customerid(customer)
        orders = orders.reverse()
        return render(request, 'orders.html', {'orders': orders})


def BootstrapFilterView(request):
    categories = Category.get_all_categories()
    cart = request.session.get('cart')
    qs = Product.objects.all()
    query = request.GET.get('q')

    qs = qs.filter(title__icontains=query)
    stuff = {
        'queryset': qs,
        'categories': categories,
        'cart': cart
    }
    return render(request, 'search.html', stuff)



class Wishlist_View(View):
    def get(self, request):
        customer = request.session.get('customer')
        wishlist_items = Wishlist.get_wishlist_by_customerid(customer)
        wishlist_items = wishlist_items.reverse()
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

    def post(self, request):
        customer = request.session.get('customer')
        product_id = request.POST.get('product')
        #print(product_id)
        products = Product.get_all_product_by_id([product_id])

        for product in products:
            wishlist = Wishlist(customer=Customer(id=customer),
                        product=product,
                        price=product.price,
                        category=product.category)
            wishlist.add_to_wishlist()

        return redirect('Nostalgia_Menu')