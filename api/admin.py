from django.contrib import admin
from .models import Customer, Cake, CakeCustomization, Cart, Order

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_no', 'city')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'flavour', 'size', 'price', 'available')
    list_filter = ('available', 'flavour', 'size')
    search_fields = ('name', 'flavour')

@admin.register(CakeCustomization)
class CakeCustomizationAdmin(admin.ModelAdmin):
    list_display = ('cake', 'message', 'egg_version', 'shape')
    list_filter = ('egg_version', 'shape')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'quantity', 'total_amount')
    list_filter = ('customer',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_price', 'order_date', 'order_status', 'payment_status')
    list_filter = ('order_status', 'payment_status', 'payment_method')
    search_fields = ('customer__first_name', 'customer__email')