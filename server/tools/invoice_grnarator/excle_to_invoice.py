from fpdf import FPDF
import pandas as pd
from datetime import datetime
import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry  # You'll need to install this: pip install tkcalendar


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

def generate_invoices(input_file, from_company, to_company, billing_month, gmt):
    try:
        # Check if file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Data file not found: {input_file}")

        # Read data
        data = pd.read_excel(input_file)

        # Validate required columns
        required_columns = ['Account id', 'Area prefix', 'Area name', 'Total duration', 'Call charges']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Convert relevant columns to appropriate data types
        data['Call charges'] = pd.to_numeric(data['Call charges'], errors='coerce')
        data['Total duration'] = pd.to_numeric(data['Total duration'], errors='coerce')
        data['Area prefix'] = data['Area prefix'].astype(str)

        # Create output directory
        output_dir = 'invoices'
        os.makedirs(output_dir, exist_ok=True)

        # Generate separate invoices for each Account ID
        unique_accounts = data['Account id'].unique()

        for account_id in unique_accounts:
            account_data = data[data['Account id'] == account_id]
            
            # Generate invoice number (you can modify this format)
            invoice_number = f"{datetime.now().strftime('%Y%m')}-{account_id}"
            
            # Calculate total amount
            total_amount = account_data['Call charges'].sum()

            # Create PDF with new design
            pdf = InvoicePDF()
            pdf.add_page()
            pdf.design_header(invoice_number, 'logo.jpg')
            pdf.add_company_details(from_company, to_company, billing_month, gmt)
            pdf.add_table(account_data[['Area prefix', 'Area name', 'Total duration', 'Call charges']])

            # Save PDF
            output_file = os.path.join(output_dir, f'Invoice_{invoice_number}.pdf')
            pdf.output(output_file)
            print(f"Invoice generated successfully: {output_file}")

    except Exception as e:
        print(f"Error generating invoices: {e}")
        sys.exit(1)


class InvoiceGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Invoice Generator")
        self.root.geometry("600x500")

        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # File Selection
        ttk.Label(main_frame, text="Input Excel File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.file_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_file).grid(row=0, column=2)

        # Company Details
        ttk.Label(main_frame, text="From Company:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.from_company = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.from_company, width=50).grid(row=1, column=1, columnspan=2, sticky=tk.W)

        ttk.Label(main_frame, text="To Company:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.to_company = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.to_company, width=50).grid(row=2, column=1, columnspan=2, sticky=tk.W)

        # Billing Month
        ttk.Label(main_frame, text="Billing Date:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.billing_date = DateEntry(main_frame, width=20, background='darkblue',
                                    foreground='white', borderwidth=2)
        self.billing_date.grid(row=3, column=1, sticky=tk.W)

        # GMT Selection
        ttk.Label(main_frame, text="Time Zone (GMT):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.gmt = tk.StringVar(value="+00:00")
        gmt_values = [f"{i:+03d}:00" for i in range(-12, 13)]
        ttk.Combobox(main_frame, textvariable=self.gmt, values=gmt_values, width=10).grid(row=4, column=1, sticky=tk.W)

        # Generate Button
        ttk.Button(main_frame, text="Generate Invoices", command=self.generate).grid(row=5, column=0, columnspan=3, pady=20)

        # Status Text
        self.status_text = tk.Text(main_frame, height=10, width=60)
        self.status_text.grid(row=6, column=0, columnspan=3, pady=10)

        # Set default values
        self.from_company.set("Telecom Provider Inc.")
        self.to_company.set("Client Company Ltd.")

    def browse_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)

    def log_message(self, message):
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.root.update()

    def generate(self):
        try:
            self.status_text.delete(1.0, tk.END)

            # Validate inputs
            if not self.file_path.get():
                raise ValueError("Please select an input file")
            if not self.from_company.get():
                raise ValueError("Please enter the From Company name")
            if not self.to_company.get():
                raise ValueError("Please enter the To Company name")

            # Get billing month in required format
            billing_month = self.billing_date.get_date().strftime("%B %Y")

            self.log_message("Starting invoice generation...")

            # Call the generate_invoices function
            generate_invoices(
                self.file_path.get(),
                self.from_company.get(),
                self.to_company.get(),
                billing_month,
                self.gmt.get()
            )

            self.log_message("Invoice generation completed successfully!")
            messagebox.showinfo("Success", "Invoices generated successfully!")

        except Exception as e:
            self.log_message(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = InvoiceGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()