from django.contrib import admin
from django.urls import path

from .views import index, Login, Signup, home 

urlpatterns = [
    path('', home, name="Nostalgia_Home"),
    path('menu', index, name="Nostalgia_Menu"),
    path('signup', Signup.as_view()),
    path('login', Login.as_view()),
]
