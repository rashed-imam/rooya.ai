from django.shortcuts import render
from rest_framework import viewsets
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_fields = ['name', 'email']
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name', 'created_at']

# Create your views here.
