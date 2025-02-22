from django.shortcuts import render
from rest_framework import viewsets
from .models import Invoice, InvoiceItem
from .serializers import InvoiceSerializer, InvoiceItemSerializer
from django.http import HttpResponse
from django.conf import settings
import os

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filterset_fields = ['status', 'customer']
    search_fields = ['invoice_number', 'customer__name']
    ordering_fields = ['issue_date', 'due_date', 'total_amount']

class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer
    filterset_fields = ['invoice']

def debug_media(request, path):
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    print(f"Requested path: {path}")
    print(f"Full path: {full_path}")
    print(f"File exists: {os.path.exists(full_path)}")
    if os.path.exists(full_path):
        print(f"File permissions: {oct(os.stat(full_path).st_mode)[-3:]}")
    return HttpResponse(f"Debug info printed to console for {path}")
