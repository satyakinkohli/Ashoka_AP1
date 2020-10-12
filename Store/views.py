from django.shortcuts import render

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


        #Validating

        error = None

        if len(password) < 6:
            error = "Password must be atleast 6 characters."



        #Saving
        if not error:
            

            customer = Customer(email = email , password = password)
            customer.register()
        else:
            return render(request , 'signup.html' , {'error' : error})