from django.db import models

class Customer(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    # other fields like phone, address, city, etc.

class Cake(models.Model):
    name = models.CharField(max_length=100)
    flavour = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='cakes/')
    available = models.BooleanField(default=True)

# Add other models (CakeCustomization, Cart, Order) similarly as per the structure.
