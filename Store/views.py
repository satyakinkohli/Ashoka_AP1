from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from .models.product import Product

from .models.category import Category


def index(request):
    products = Product.get_all_product()
    categories = Category.get_all_categories()
    data = {}
    data['products'] = products
    data['categories'] = categories

    return render(request, 'index.html', data)
    # return HttpResponse("Request Received")

