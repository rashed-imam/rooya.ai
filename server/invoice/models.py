from django.db import models
from django.conf import settings
from crm.models import Customer
from django.core.exceptions import ValidationError
import pandas as pd

class Invoice(models.Model):
    excel_file = models.FileField(upload_to='excel_files/')
    from_company = models.CharField(max_length=255, default="Telecom Provider Inc.")
    to_company = models.CharField(max_length=255, default="Client Company Ltd.")
    billing_date = models.DateField()
    gmt = models.CharField(max_length=6, default="+00:00")
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='invoices/', blank=True, null=True)

    def __str__(self):
        return f"Invoice {self.created_at.strftime('%Y-%m-%d')}"

    def clean(self):
        if self.excel_file:
            try:
                df = pd.read_excel(self.excel_file)
                required_columns = ['Account id', 'Area prefix', 'Area name', 'Total duration', 'Call charges']
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    raise ValidationError(f"Excel file missing required columns: {missing_columns}")
            except Exception as e:
                raise ValidationError(f"Invalid Excel file: {str(e)}")

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.description} - {self.invoice.invoice_number}"
