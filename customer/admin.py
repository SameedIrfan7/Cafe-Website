from django.contrib import admin
from customer.models import Customer, Orders, Cart
# Register your models here.


admin.site.register(Customer)
admin.site.register(Orders)
admin.site.register(Cart)
