from django.shortcuts import render

from rest_framework import viewsets
from .models import Customer, Cake
from .serializers import CustomerSerializer, CakeSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CakeViewSet(viewsets.ModelViewSet):
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer

