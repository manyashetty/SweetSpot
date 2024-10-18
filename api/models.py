from django.db import models

class Customer(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Cake(models.Model):
    name = models.CharField(max_length=200)
    flavour = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='cakes/')
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.flavour}"

class CakeCustomization(models.Model):
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, related_name='customizations')
    message = models.CharField(max_length=200)
    egg_version = models.BooleanField(default=True)
    toppings = models.CharField(max_length=200)
    shape = models.CharField(max_length=50)

    def __str__(self):
        return f"Customization for {self.cake.name}"

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts')
    cakes = models.ManyToManyField(Cake, related_name='carts')
    quantity = models.PositiveIntegerField(default=1)
    customization = models.ForeignKey(
        CakeCustomization, 
        on_delete=models.SET_NULL,  
        null=True, 
        blank=True,
        related_name='carts'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Cart for {self.customer.first_name}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )
    PAYMENT_METHOD_CHOICES = (
        ('CASH', 'Cash on Delivery'),
        ('CARD', 'Credit/Debit Card'),
        ('UPI', 'UPI'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    cake_customization = models.ForeignKey(
        CakeCustomization, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    items = models.ManyToManyField(Cart, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField()
    order_status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    payment_status = models.CharField(
        max_length=50,
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING'
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        default='CASH'
    )

    def __str__(self):
        return f"Order #{self.id} by {self.customer.first_name}"