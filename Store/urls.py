from django.contrib import admin
from django.urls import path

from .views import index, signup, login, home

urlpatterns = [
    path('', home, name="Nostalgia_Home"),
    path('menu', index, name="Nostalgia_Menu"),
    path('signup', signup),
    path('login', login),
]
