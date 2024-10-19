from rest_framework import serializers
from .models import Customer, Cake, CakeCustomization, Cart, Order

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
    def validate_phone_no(self, value):
        if not value.isdigit() or not (10 <= len(value) <= 15):
            raise serializers.ValidationError("Invalid phone number.")
        return value

    def validate_pincode(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Invalid pincode.")
        return value

class CakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cake
        fields = '__all__'

class CakeCustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeCustomization
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    cakes = serializers.PrimaryKeyRelatedField(many=True, queryset=Cake.objects.all())
    customization = serializers.PrimaryKeyRelatedField(queryset=CakeCustomization.objects.all(), allow_null=True, required=False)
    
    class Meta:
        model = Cart
        fields = ['id', 'customer', 'cakes', 'quantity', 'customization', 'total_amount']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'