from django.db import models

# Create your models here.

class SellerTable(models.Model):
    gst_number = models.CharField(max_length= 255)
    seller_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    profile_pic = models.FileField(upload_to='seller_profiles', default='sad.jpg')

    def __str__(self):
        return self.seller_name

class CategoryTable(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name
    


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    image = models.FileField(upload_to='product_pics', default='chair.avif')
    des = models.TextField()
    price = models.FloatField(default=1.0)
    stock = models.IntegerField()
    seller = models.ForeignKey(SellerTable, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryTable, on_delete=models.CASCADE)


    def __str__(self):
        return self.product_name
    

