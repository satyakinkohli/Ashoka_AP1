from django.contrib import admin
from django.urls import path

from .views import Index, Login, Signup, home, logout, Cart

urlpatterns = [
    path('', home, name="Nostalgia_Home"),
    path('menu', Index.as_view(), name="Nostalgia_Menu"),
    path('signup', Signup.as_view()),
    path('login', Login.as_view()),
    path('logout', logout, name='logout'),
    path('cart', Cart.as_view(), name='cart'),
]
