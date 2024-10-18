from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Customer, Cake, CakeCustomization, Cart, Order
from .serializers import (CustomerSerializer, CakeSerializer, 
                        CakeCustomizationSerializer, CartSerializer, 
                        OrderSerializer, AddToCartSerializer,PlaceOrderSerializer)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            customer = Customer.objects.get(email=email, password=password)
            return Response({"message": "Login Successful"})
        except Customer.DoesNotExist:
            return Response({"message": "Invalid credentials"}, status=400)

class CakeViewSet(viewsets.ModelViewSet):
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer

class CakeCustomizationViewSet(viewsets.ModelViewSet):
    queryset = CakeCustomization.objects.all()
    serializer_class = CakeCustomizationSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get validated data
        cake_id = serializer.validated_data['cake_id']
        quantity = serializer.validated_data['quantity']
        needs_customization = serializer.validated_data['customization']

        # Check if cake exists and is available
        try:
            cake = Cake.objects.get(id=cake_id)
            if not cake.available:
                return Response(
                    {"error": "This cake is currently not available"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Cake.DoesNotExist:
            return Response(
                {"error": "Cake not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # needs auth
        customer_id = request.data.get('customer_id')  # For testing purposes
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Handle customization if requested
        customization = None
        if needs_customization:
            if not all(field in serializer.validated_data for field in ['message', 'egg_version', 'toppings', 'shape']):
                return Response(
                    {"error": "All customization fields are required when customization is True"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            customization = CakeCustomization.objects.create(
                cake=cake,
                message=serializer.validated_data['message'],
                egg_version=serializer.validated_data['egg_version'],
                toppings=serializer.validated_data['toppings'],
                shape=serializer.validated_data['shape']
            )

        # Calculate total amount
        total_amount = cake.price * quantity

        # Create or update cart
        try:
            cart = Cart.objects.get(customer=customer)
            cart.cakes.add(cake)
            cart.quantity = quantity
            if customization:
                cart.customization = customization
            cart.total_amount = total_amount
            cart.save()
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                customer=customer,
                quantity=quantity,
                customization=customization,
                total_amount=total_amount
            )
            cart.cakes.add(cake)

        response_data = {
            "message": "Successfully added to cart",
            "cart_id": cart.id,
            "cake": CakeSerializer(cake).data,
            "quantity": quantity,
            "total_amount": str(total_amount)
        }

        if customization:
            response_data["customization"] = CakeCustomizationSerializer(customization).data

        return Response(response_data, status=status.HTTP_201_CREATED)

    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['post'])
    def place_order(self, request):
        serializer = PlaceOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get validated data
        cake_id = serializer.validated_data['cake_id']
        delivery_address = serializer.validated_data['delivery_address']
        payment_method = serializer.validated_data['payment_method']

        #need to authenticate
        customer_id = request.data.get('customer_id')  # For testing purposes
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if cake exists in customer's cart
        try:
            cart = Cart.objects.get(
                customer=customer,
                cakes__id=cake_id
            )
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cake not found in cart"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if cake is still available
        cake = get_object_or_404(Cake, id=cake_id)
        if not cake.available:
            return Response(
                {"error": "Cake is no longer available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    customer=customer,
                    cake_customization=cart.customization,
                    quantity=cart.quantity,
                    total_price=cart.total_amount,
                    delivery_address=delivery_address,
                    order_status='PENDING',
                    payment_status='PENDING',
                    payment_method=payment_method
                )
                
                # Add cart to order items
                order.items.add(cart)

                # Clear the cart 
                cart.cakes.remove(cake)
                if cart.cakes.count() == 0:
                    cart.delete()

                # Serialize the order for response
                order_serializer = OrderSerializer(order)
                
                return Response({
                    "message": "Order placed successfully",
                    "order": order_serializer.data
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "error": "Failed to place order",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=False, methods=['get'])
    def order_history(self, request):
        customer_id = request.query_params.get('customer_id')  #
        
        if not customer_id:
            return Response(
                {"error": "Customer ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        orders = Order.objects.filter(customer=customer).order_by('-order_date')
        serializer = OrderSerializer(orders, many=True)
        
        return Response(serializer.data)
