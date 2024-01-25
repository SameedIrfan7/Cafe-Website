from django.contrib import admin
from seller.models import SellerTable, Product, CategoryTable
# Register your models here.
admin.site.register(SellerTable)
admin.site.register(CategoryTable)
admin.site.register(Product)