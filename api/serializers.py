from rest_framework import serializers
from .models import Customer, Cake, CakeCustomization, Cart, Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cake
        fields = '__all__'

class CakeCustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeCustomization
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class AddToCartSerializer(serializers.Serializer):
    cake_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    customization = serializers.BooleanField(default=False)
    message = serializers.CharField(required=False, allow_blank=True)
    egg_version = serializers.BooleanField(required=False)
    toppings = serializers.CharField(required=False, allow_blank=True)
    shape = serializers.CharField(required=False, allow_blank=True)

class PlaceOrderSerializer(serializers.Serializer):
    cake_id = serializers.IntegerField()
    delivery_address = serializers.CharField(required=True)
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_METHOD_CHOICES)