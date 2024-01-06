from django.db import models


class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    profile_pic = models.FileField(upload_to="customer_pics", default="sad.jpg")
    mobile = models.CharField(max_length=255)
    address = models.CharField(max_length=255, default=' ')
    

    def __str__(self):
        return self.full_name
    
class Category(models.Model):
    C_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.C_name
    
class Food(models.Model):
    Name= models.CharField(max_length=255)
    Description = models.CharField(max_length=255)
    Price = models.CharField(max_length=255)
    Stack = models.CharField(max_length=255)
    Categogy_id = models.CharField(max_length=255)

    def __str__(self):
        return self.Name
    
    

   
  