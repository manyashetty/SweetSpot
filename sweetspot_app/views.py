from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import Customer, Cake, CakeCustomization, Cart, Order
from .serializers import CustomerSerializer, CakeSerializer, CakeCustomizationSerializer, CartSerializer, OrderSerializer, LoginSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    @action(detail=False, methods=['post'])
    def login(self, request):
        # Use the LoginSerializer to validate the input
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Check if the customer exists
            try:
                customer = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

            # Verify the password
            if check_password(password, customer.password):  # Assuming password is hashed
                return Response({"message": "Login Successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CakeViewSet(viewsets.ModelViewSet):
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer

class CakeCustomizationViewSet(viewsets.ModelViewSet):
    queryset = CakeCustomization.objects.all()
    serializer_class = CakeCustomizationSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'], url_path='add_to_cart')
    def add_to_cart(self, request):
        customer_id = request.data.get('customer')
        cake_id = request.data.get('cake')
        customization_id = request.data.get('customization', None)
        quantity = request.data.get('quantity', 1)

        # Validate customer exists
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        # Step 1: Check if the cake exists and is available
        try:
            cake = Cake.objects.get(id=cake_id)
            if not cake.available:
                return Response({"error": "This cake is not available."}, status=status.HTTP_400_BAD_REQUEST)
        except Cake.DoesNotExist:
            return Response({"error": "Cake not found."}, status=status.HTTP_404_NOT_FOUND)

        # Step 2: Handle customization (optional)
        if customization_id:
            try:
                customization = CakeCustomization.objects.get(id=customization_id, customer=customer, cake=cake)
            except CakeCustomization.DoesNotExist:
                return Response({"error": "Cake customization not found for this customer and cake."}, status=status.HTTP_404_NOT_FOUND)
        else:
            customization = None

        # Step 3: Get or create the cart for the customer
        cart, created = Cart.objects.get_or_create(customer=customer)

        # Step 4: Add the cake to the cart
        cart.cakes.add(cake)
        cart.quantity += int(quantity)
        if customization:
            cart.customization = customization
        cart.total_amount += cake.price * int(quantity)
        cart.save()

        return Response({"message": "Cake added to the cart successfully!"}, status=status.HTTP_200_OK)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'], url_path='place_order')
    def place_order(self, request):
        customer_id = request.data.get('customer')

        # Validate customer exists
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get the cart for the customer
        try:
            cart = Cart.objects.get(customer=customer)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        if not cart.cakes.exists():
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = Order.objects.create(
            customer=customer,
            cake_customization=cart.customization,
            quantity=cart.quantity,
            total_price=cart.total_amount,
            delivery_address=customer.address,
            order_status="Pending",
            payment_status="Pending",
            payment_method="Card"  # You might want to make this dynamic based on input
        )

        # Add items to the order
        for cake in cart.cakes.all():
            order.items.add(cake)

        order.save()

        # Clear the cart after placing the order
        cart.cakes.clear()
        cart.quantity = 0
        cart.customization = None
        cart.total_amount = 0.00
        cart.save()

        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

