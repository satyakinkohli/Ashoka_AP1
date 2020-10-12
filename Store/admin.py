from django.contrib import admin

from .models.product import Product
from .models.category import Category
from .models.customer import Customer


class AdminProduct(admin.ModelAdmin):
    list_display = ['title', 'price', 'availability', 'category', 'rating', 'no_of_reviews','image']


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)

