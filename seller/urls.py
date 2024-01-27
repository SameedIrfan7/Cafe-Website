from django.urls import path
from seller.views import *

urlpatterns = [
    path('', index_view, name='seller_index'),
    path('register/', register_view, name="seller_register"),
    path('login/', login_view, name="seller_login"),
    path('otp/', otp_view, name="seller_otp"),
    path('logout/', logout_view, name='seller_logout'),
    path('add_product/', add_product, name='add_product'),
    path('inventory/', inventory_view, name='inventory'),
    path('edit_product/<int:pk>', edit_product, name='edit_product')
   
]