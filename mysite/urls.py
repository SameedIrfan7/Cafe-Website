"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
<<<<<<< HEAD
from customer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home , name="home"),
    path('about/', about , name="about"),
    path('contact/', contact , name="contact"),
    path('menu/', menu , name="menu"),
    path('single/', single , name="single"),
    path('login/', login , name="login"),
    path('register/', register , name="register"),
    path('header/', header , name="header"),
    path('verification/',otp,name='otp')
=======

urlpatterns = [
    path('admin/', admin.site.urls),
>>>>>>> 7bd1ddb8542b68a91eb1d655f7d91b32ca367ab7
]
