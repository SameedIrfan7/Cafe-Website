from django.db import models

# Create your models here.
class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length=255)
    profile_pic =  models.FileField(upload_to='customer_profile',default='sad.jpg')
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    
    #this function returns the value of what it has returned in the dailog box or table of database
    def __str__(self):
        return self.full_name