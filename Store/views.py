from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from .models.product import Product

from .models.category import Category


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
    return render(request, 'signup.html')