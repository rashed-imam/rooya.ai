from rest_framework import serializers
from .models import Invoice, InvoiceItem
from crm.serializers import CustomerSerializer

class InvoiceItemSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = InvoiceItem
        fields = ['id', 'description', 'quantity', 'unit_price', 'total']

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    customer_details = CustomerSerializer(source='customer', read_only=True)
    
    class Meta:
        model = Invoice
        fields = ['id', 'customer', 'customer_details', 'invoice_number', 
                 'issue_date', 'due_date', 'total_amount', 'status', 
                 'items', 'created_at', 'updated_at']