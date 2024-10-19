from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework import viewsets, status
from decimal import Decimal
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import Customer, Cake, CakeCustomization, Cart, Order
from .serializers import CustomerSerializer, CakeSerializer, CakeCustomizationSerializer, CartSerializer, OrderSerializer, LoginSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    def create(self, request, *args, **kwargs):
        # Validate phone number
        phone_no = request.data.get('phone_no')
        if not self.is_valid_phone_number(phone_no):
            return Response({"error": "Invalid phone number."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate pincode
        pincode = request.data.get('pincode')
        if not self.is_valid_pincode(pincode):
            return Response({"error": "Invalid pincode."}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with creating the customer
        return super().create(request, *args, **kwargs)

    def is_valid_phone_number(self, phone_no):
        # Check if the phone number is numeric and of correct length
        return phone_no.isdigit() and (10 <= len(phone_no) <= 15)

    def is_valid_pincode(self, pincode):
        # Check if the pincode is numeric and of correct length (usually 6)
        return pincode.isdigit() and len(pincode) == 6
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], authentication_classes=[])
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
        customization = None
        if customization_id:
            try:
                customization = CakeCustomization.objects.get(id=customization_id, customer=customer, cake=cake)
            except CakeCustomization.DoesNotExist:
                return Response({"error": "Cake customization not found or does not belong to this customer."}, status=status.HTTP_404_NOT_FOUND)

        # Step 3: Get or create the cart for the customer
        cart, created = Cart.objects.get_or_create(customer=customer)

        # Step 4: Check if the cake is already in the cart
        if cake in cart.cakes.all():
            # Update quantity if the cake already exists in the cart
            cart.quantity += int(quantity)
        else:
            # Add the cake to the cart if not present
            cart.cakes.add(cake)
            cart.quantity = int(quantity)

        # Step 5: Add customization (if present) and update total amount
        if customization:
            cart.customization = customization
        cart.total_amount += Decimal(cake.price) * int(quantity)
        cart.save()

        return Response({"message": "Cake added to the cart successfully!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], url_path='update_cart')
    def update_cart(self, request, pk=None):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        # Fetch data from request
        cakes_data = request.data.get('cakes', [])
        customization_id = request.data.get('customization', None)
        quantity = request.data.get('quantity', 1)

        # Update cakes in the cart
        cakes = Cake.objects.filter(id__in=cakes_data)
        cart.cakes.set(cakes)

        # Update customization if provided
        if customization_id:
            try:
                customization = CakeCustomization.objects.get(id=customization_id)
                cart.customization = customization
            except CakeCustomization.DoesNotExist:
                return Response({'error': 'Customization not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            cart.customization = None  # If no customization, set to None

        # Update the quantity and total_amount
        cart.quantity = quantity
        total_amount = sum(Decimal(cake.price) * int(quantity) for cake in cakes)
        cart.total_amount = total_amount

        # Save the updated cart
        cart.save()

        # Serialize the updated cart and return the response
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'], url_path='delete_cart')
    def delete_cart(self, request, pk=None):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        # Optional: If you want to delete only specific cakes from the cart, use this section
        cake_ids = request.data.get('cakes', [])
        if cake_ids:
            cakes_to_remove = Cake.objects.filter(id__in=cake_ids)
            cart.cakes.remove(*cakes_to_remove)

            # If all cakes are removed, reset the quantity and total amount
            if not cart.cakes.exists():
                cart.quantity = 0
                cart.total_amount = 0
            else:
                cart.total_amount = sum(Decimal(cake.price) * cart.quantity for cake in cart.cakes.all())

            cart.save()
            return Response({"message": "Cakes removed from the cart successfully."}, status=status.HTTP_200_OK)
        else:
            # If no cake IDs provided, delete the whole cart
            cart.delete()
            return Response({"message": "Cart deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    
    @action(detail=False, methods=['post'], url_path='place_order')
    def place_order(self, request):
        customer_id = request.data.get('customer')

        # Validate customer exists
        customer = get_object_or_404(Customer, id=customer_id)

        # Get the cart for the customer
        cart = get_object_or_404(Cart, customer=customer)

        # Check if cart is empty
        if not cart.cakes.exists():
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Check availability of cakes in the cart
        unavailable_cakes = [cake for cake in cart.cakes.all() if not cake.available]

        if unavailable_cakes:
            return Response(
                {"error": f"The following cakes are not available: {[cake.name for cake in unavailable_cakes]}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the order
        order = Order.objects.create(
            customer=customer,
            cake_customization=cart.customization,
            quantity=cart.quantity,
            total_price=cart.total_amount,
            delivery_address=customer.address,
            order_status="Pending",
            payment_status="Pending"
        )

        # Add cakes to the order
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