from fpdf import FPDF
import pandas as pd
from datetime import datetime
import os
from django.conf import settings
from .models import Invoice

class InvoicePDF(FPDF):
    def design_header(self, invoice_number, logo_path=None):
        # Header with logo and title
        if logo_path and os.path.exists(logo_path):
            self.image(logo_path, 10, 10, 20, 20)  # Logo with fixed size 100x100px
        
        # Invoice title on right
        self.set_font('Arial', 'B', 24)
        self.set_xy(120, 15)
        self.cell(80, 10, 'Invoice', 0, 1, 'R')
        
        # Add horizontal line
        self.line(10, 35, 200, 35)
        
        # Date and Invoice number row
        self.set_xy(10, 40)
        self.set_font('Arial', 'B', 10)
        self.cell(90, 10, f'Date: {datetime.now().strftime("%d/%m/%Y")}', 0, 0, 'L')
        self.cell(90, 10, f'Invoice No: {invoice_number}', 0, 1, 'R')
        
        # Another horizontal line
        self.line(10, 55, 200, 55)

    def add_company_details(self, from_company, to_company, billing_month, gmt):
        # Company details in two columns with better spacing
        self.set_xy(10, 60)
        
        # Left column - Invoiced To
        self.set_font('Arial', 'B', 10)
        self.cell(90, 8, 'Invoiced To:', 0, 1, 'L')
        self.set_font('Arial', '', 9)
        self.set_xy(10, 68)  # Fixed position for invoiced to details
        self.multi_cell(80, 5, to_company, 0, 'L')  # Reduced width to 80
        
        # Right column - Pay To (with adjusted position)
        self.set_xy(120, 60)  # Moved further right
        self.set_font('Arial', 'B', 10)
        self.cell(80, 8, 'Pay To:', 0, 1, 'L')
        self.set_font('Arial', '', 9)
        self.set_xy(120, 68)  # Fixed position for pay to details
        self.multi_cell(80, 5, f"{from_company}\nBilling Month: {billing_month}\nTime Zone: GMT {gmt}", 0, 'L')
        
        # Reset position for table with more space
        self.set_xy(10, 100)  # Increased spacing before table

    def add_table(self, data):
        # Table headers with light gray background
        self.set_fill_color(240, 240, 240)
        self.set_font('Arial', 'B', 10)
        
        # Column widths and headers
        cols = [('SN', 15), ('Area Prefix', 30), ('Area Name', 60), 
                ('Duration', 40), ('Charge', 40)]
        
        # Header row
        for title, width in cols:
            self.cell(width, 10, title, 1, 0, 'C', True)
        self.ln()

        # Data rows
        self.set_font('Arial', '', 9)
        total_duration = 0
        total_charges = 0
        
        for idx, row in data.iterrows():
            duration = row['Total duration'] / 60
            total_duration += duration
            total_charges += row['Call charges']
            
            self.cell(15, 8, str(idx + 1), 1, 0, 'C')
            self.cell(30, 8, str(row['Area prefix']), 1, 0, 'C')
            self.cell(60, 8, str(row['Area name']), 1, 0, 'L')
            self.cell(40, 8, f"{duration:.2f} min", 1, 0, 'R')
            self.cell(40, 8, f"${row['Call charges']:.2f}", 1, 1, 'R')

        # Totals section
        self.ln(5)
        self.set_font('Arial', 'B', 10)
        
        # Subtotal
        self.cell(145, 8, 'Sub Total:', 0, 0, 'R')
        self.cell(40, 8, f"${total_charges:.2f}", 0, 1, 'R')
        
        # Tax (10%)
        tax = total_charges * 0.10
        self.cell(145, 8, 'Tax (10%):', 0, 0, 'R')
        self.cell(40, 8, f"${tax:.2f}", 0, 1, 'R')
        
        # Total with tax
        self.set_font('Arial', 'B', 12)
        self.cell(145, 10, 'Total:', 0, 0, 'R')
        self.cell(40, 10, f"${(total_charges + tax):.2f}", 0, 1, 'R')

    def footer(self):
        # Move to bottom of page
        self.set_y(-30)
        
        # Add note
        self.set_font('Arial', '', 8)
        self.cell(0, 10, 'NOTE: This is computer generated receipt and does not require physical signature.', 0, 0, 'C')
        
        # Page number
        self.set_y(-20)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_invoice_pdfs(invoice_obj):
    try:
        # Read data from the uploaded Excel file
        data = pd.read_excel(invoice_obj.excel_file.path)
        
        # Convert numeric columns to appropriate types
        data['Total duration'] = pd.to_numeric(data['Total duration'], errors='coerce')
        data['Call charges'] = pd.to_numeric(data['Call charges'], errors='coerce')
        data['Account id'] = data['Account id'].astype(str)  # Ensure Account ID is string

        # Create output directory within media
        output_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
        os.makedirs(output_dir, exist_ok=True)

        # Generate separate invoices for each Account ID
        unique_accounts = data['Account id'].unique()
        
        for account_id in unique_accounts:
            account_data = data[data['Account id'] == account_id].copy()
            
            # Clean the account_id for filename (remove special characters)
            safe_account_id = "".join(c for c in account_id if c.isalnum() or c in ('-', '_')).strip()
            
            # Generate invoice number with cleaned account ID
            invoice_number = f"{invoice_obj.billing_date.strftime('%Y%m')}-{safe_account_id}"
            
            # Create PDF
            pdf = InvoicePDF()
            pdf.add_page()
            
            # Get logo path from static files
            logo_path = os.path.join(settings.STATIC_ROOT, 'logo.jpg')
            
            pdf.design_header(invoice_number, logo_path if os.path.exists(logo_path) else None)
            pdf.add_company_details(
                invoice_obj.from_company,
                invoice_obj.to_company,
                invoice_obj.billing_date.strftime("%B %Y"),
                invoice_obj.gmt
            )
            
            # Format numeric columns before adding to table
            table_data = account_data[['Area prefix', 'Area name', 'Total duration', 'Call charges']].copy()
            table_data['Total duration'] = table_data['Total duration'].round(2)
            table_data['Call charges'] = table_data['Call charges'].round(2)
            
            pdf.add_table(table_data)

            # Create filename and ensure directory exists
            filename = f'Invoice_{invoice_number}.pdf'
            output_file = os.path.join(output_dir, filename)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Save PDF
            pdf.output(output_file)
            
            # Update the model with the PDF file path
            relative_path = f'invoices/{filename}'
            invoice_obj.pdf_file = relative_path
            invoice_obj.save()

            print(f"Generated PDF at: {output_file}")  # Debug print

    except Exception as e:
        print(f"Detailed error: {str(e)}")  # Add detailed logging
        raise Exception(f"Error generating invoices: {str(e)}") 