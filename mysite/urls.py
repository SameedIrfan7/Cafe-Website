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
from django.urls import path, include
from django.conf.urls.static import static
from customer.views import *
from django.conf import settings

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
    path('verification/',otp,name='otp'),
    path('logout/', logout, name='logout'),
    path('cart/', cart, name='cart'),
    path('add_to_cart/<int:pk>', add_to_cart, name='add_to_cart'),
    path('del_cart/<int:pk>', del_cart, name='del_cart'),
    path('cart/paymenthandler/', paymenthandler, name='paymenthandler'),
    path('seller/', include('seller.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
