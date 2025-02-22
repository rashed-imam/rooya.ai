from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.conf import settings
import os
from .models import Invoice
from .utils import generate_invoice_pdfs

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'from_company', 'to_company', 'billing_date', 'download_pdf']
    readonly_fields = ['created_at', 'pdf_file', 'generated_pdfs']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        generate_invoice_pdfs(obj)

    def download_pdf(self, obj):
        if obj.pdf_file:
            # Get all PDFs in the invoices directory
            invoice_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
            if os.path.exists(invoice_dir):
                pdfs = [f for f in os.listdir(invoice_dir) if f.endswith('.pdf')]
                if pdfs:
                    # Return link to the first PDF found
                    pdf_url = f"{settings.MEDIA_URL}invoices/{pdfs[0]}"
                    return format_html('<a href="{}" target="_blank">Download PDF</a>', pdf_url)
        return "No PDF available"
    download_pdf.short_description = "Invoice PDF"

    def generated_pdfs(self, obj):
        """Display all PDFs generated for this invoice"""
        invoice_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
        if not os.path.exists(invoice_dir):
            return "No PDFs generated yet"
            
        # List all PDF files in the directory
        pdf_files = [f for f in os.listdir(invoice_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            return "No PDFs found"
            
        pdf_links = []
        for pdf in pdf_files:
            # Create the correct URL for each PDF
            pdf_url = f"{settings.MEDIA_URL}invoices/{pdf}"
            # Check if file exists
            pdf_path = os.path.join(invoice_dir, pdf)
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path) / 1024  # Convert to KB
                pdf_links.append(
                    f'<div style="margin: 5px 0; padding: 8px; background-color: #f5f5f5; '
                    f'border-radius: 4px; display: flex; justify-content: space-between; align-items: center;">'
                    f'<span>📄 {pdf} ({file_size:.1f} KB)</span>'
                    f'<a href="{pdf_url}" target="_blank" '
                    f'style="background-color: #447e9b; color: white; padding: 4px 8px; '
                    f'border-radius: 3px; text-decoration: none;">Download</a>'
                    f'</div>'
                )
        
        return mark_safe('<div style="max-height: 400px; overflow-y: auto;">' + 
                        ''.join(pdf_links) + '</div>')
    generated_pdfs.short_description = "Generated PDFs"

    fieldsets = (
        (None, {
            'fields': ('excel_file', 'from_company', 'to_company', 
                      'billing_date', 'gmt', 'created_at')
        }),
        ('Generated Documents', {
            'fields': ('generated_pdfs',),
            'classes': ('collapse',)
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/custom.css',)
        }
