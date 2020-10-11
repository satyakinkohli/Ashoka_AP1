from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from .models.product import Product


def index(request):
    products = Product.get_all_product()

    return render(request, 'index.html', {'products': products})
    # return HttpResponse("Request Received")

