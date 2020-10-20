from django.contrib import admin
from django.urls import path

from .views import Index, Login, Signup, home, logout, Cart, checkout, Order_View, BootstrapFilterView , Wishlist_View

urlpatterns = [
    path('', home, name="Nostalgia_Home"),
    path('menu', Index.as_view(), name="Nostalgia_Menu"),
    path('signup', Signup.as_view()),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('cart', Cart.as_view(), name='cart'),
    path('checkout', checkout, name='checkout'),
    path('orders', Order_View.as_view(), name='orders'),
    path('search', BootstrapFilterView, name='search'),
    path('wishlist' , Wishlist_View.as_view(), name='wishlist'),
]
