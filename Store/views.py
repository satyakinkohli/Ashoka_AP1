from itertools import count

from django.shortcuts import render, redirect , HttpResponseRedirect
# from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext

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
        customer = request.session.get('customer')
        customer_correct = Customer.get_customer_through_id(customer)

        if not cart:
            request.session.cart = {}

        products = None
        categories = Category.get_all_categories()

        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_product_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()

        data = {'products': products, 'categories': categories, 'customer_correct' :customer_correct}

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
            customer = request.session.get('customer')
            customer_correct = Customer.get_customer_through_id(customer)

            return render(request, 'cart.html', {'products': products,'customer_correct': customer_correct})


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
    customer = request.session.get('customer')
    customer_correct = Customer.get_customer_through_id(customer)

    qs = qs.filter(title__icontains=query)
    stuff = {
        'queryset': qs,
        'categories': categories,
        'cart': cart,
        'customer_correct': customer_correct,
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
        products = Product.get_all_product_by_id([product_id])

        for product in products:
            wishlist = Wishlist(customer=Customer(id=customer),
                                product=product,
                                price=product.price,
                                category=product.category)

            if wishlist.one_wishlist_item_per_customer():
                pass
            else:
                wishlist.add_to_wishlist()

        return redirect('Nostalgia_Menu')


class Profile(View):
    def get(self, request):
        customer = request.session.get('customer')
        customer_correct = Customer.get_customer_through_id(customer)

        things = {
            'customer': customer_correct,
        }

        return render(request, 'profile.html', things)

    def post(self, request):
        new_data = request.POST
        fname = new_data.get('fname')
        mobile = new_data.get('mobile')
        address = new_data.get('address')

        customer = request.session.get('customer')
        customer_correct = Customer.get_customer_through_id(customer)

        saved_values = {
            'fname': fname,
            'mobile': mobile,
            'address': address,
        }

        print(saved_values)

        error = None

        if len(str(mobile)) != 10:
            error = "Your profile has not been updated. Please input a valid 10 digit mobile number."
        # mobile = int(mobile)
        # print(type(mobile))

        if not error:
            if fname != customer_correct.fname:
                customer_correct.fname = fname
            if mobile != customer_correct.mobile:
                customer_correct.mobile = mobile
            if address != customer_correct.address:
                customer_correct.address = address
            customer_correct.register()

            return redirect("profile")
        else:
            data = {'error': error, 'saved_values': saved_values}
            return render(request, 'profile.html', data)


class Removal_Wishlist(View):
    def post(self, request):
        wishlist_id = request.POST.get('removed')
        wishlist_instance = Wishlist.objects.filter(id=wishlist_id)
        wishlist_instance.delete()
        return redirect('wishlist')


class Removal_Cart(View):
    def post(self, request):
        product_id = request.POST.get('removed_cart')
        cart = request.session.get('cart')
        cart.pop(product_id)
        request.session['cart'] = cart

        return redirect('cart')


class Transfer_from_Cart(View):
    def post(self, request):
        product_id = request.POST.get('transferred')
        cart = request.session.get('cart')
        customer = request.session.get('customer')
        if customer:
            cart.pop(product_id)
        else:
            pass
            
            
        request.session['cart'] = cart
        customer = request.session.get('customer')
        products = Product.get_all_product_by_id([product_id])

        for product in products:
            wishlist = Wishlist(customer=Customer(id=customer),
                                product=product,
                                price=product.price,
                                category=product.category)

            if wishlist.one_wishlist_item_per_customer():
                pass
            else:
                wishlist.add_to_wishlist()

        return redirect('cart')


class Transfer_from_Wishlist(View):
    def post(self, request):
        wishlist_id = request.POST.get('transferred_wishlist')
        wishlist_instance = Wishlist.objects.filter(id=wishlist_id)

        for item in wishlist_instance:
            product_id = item.product.id

        wishlist_instance.delete()

        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(product_id)
            if quantity:
                cart[product_id] = quantity + 1
            else:
                cart[product_id] = 1
        else:
            cart = {product_id: 1}

        request.session['cart'] = cart

        return redirect('wishlist')



