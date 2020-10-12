from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

from .models.product import Product

from .models.category import Category

from .models.customer import Customer


def index(request):
    categories = Category.get_all_categories()

    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_product_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()

    data = {'products': products, 'categories': categories}

    return render(request, 'index.html', data)


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
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
            customer.register()
            return redirect("Nostalgia_Home")
        else:
            data = {'error': error, 'saved_value': saved_value}
            return render(request, 'signup.html', data)
