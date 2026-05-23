"""
Generate sample invoice document for demo purposes.
Creates a realistic-looking invoice image that can be used to test OCR extraction.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_invoice():
    """Create a sample commercial invoice image"""
    
    # Create white canvas
    width, height = 2480, 3508  # A4 at 300 DPI
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a monospace font, fallback to default
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        font_bold = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
            font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_bold = ImageFont.load_default()

    # Border
    draw.rectangle([60, 60, width-60, height-60], outline='black', width=3)
    
    # Header
    y = 100
    draw.text((120, y), "COMMERCIAL INVOICE", fill='black', font=font_large)
    y += 80
    draw.line([(120, y), (width-120, y)], fill='black', width=2)
    
    # Company Info (Seller/Shipper)
    y += 40
    draw.text((120, y), "Shipper / Exporter:", fill='gray', font=font_small)
    y += 40
    draw.text((120, y), "SHANGHAI ELECTRONICS TRADING CO., LTD", fill='black', font=font_medium)
    y += 50
    draw.text((120, y), "No. 88 Pudong Avenue, Shanghai 200120, China", fill='black', font=font_small)
    y += 40
    draw.text((120, y), "Tel: +86-21-5888-7766  Fax: +86-21-5888-7700", fill='black', font=font_small)
    
    # Invoice Details (right side)
    draw.text((1400, 220), "Invoice No: INV-2026-00451", fill='black', font=font_medium)
    draw.text((1400, 270), "Invoice Date: 15/May/2026", fill='black', font=font_medium)
    draw.text((1400, 320), "Currency: USD", fill='black', font=font_medium)
    
    # Consignee
    y += 80
    draw.line([(120, y), (width-120, y)], fill='gray', width=1)
    y += 30
    draw.text((120, y), "Consignee / Buyer:", fill='gray', font=font_small)
    y += 40
    draw.text((120, y), "PT NUSANTARA TEKNOLOGI INDONESIA", fill='black', font=font_medium)
    y += 50
    draw.text((120, y), "Jl. Sudirman Kav. 52-53, Jakarta 12190, Indonesia", fill='black', font=font_small)
    y += 40
    draw.text((120, y), "NPWP: 01.234.567.8-012.000", fill='black', font=font_small)
    
    # Shipping Details
    y += 80
    draw.line([(120, y), (width-120, y)], fill='gray', width=1)
    y += 30
    draw.text((120, y), "Country of Origin: CHINA", fill='black', font=font_medium)
    y += 50
    draw.text((120, y), "Port of Loading: SHANGHAI, CHINA", fill='black', font=font_medium)
    y += 50
    draw.text((120, y), "Port of Discharge: TANJUNG PRIOK, JAKARTA", fill='black', font=font_medium)
    y += 50
    draw.text((120, y), "Vessel: MV EVER GOLDEN", fill='black', font=font_medium)
    y += 50
    draw.text((120, y), "B/L No: SHAJKT-2026-08815", fill='black', font=font_medium)
    
    # Table Header
    y += 80
    draw.line([(120, y), (width-120, y)], fill='black', width=2)
    y += 15
    
    # Table columns
    cols = [120, 400, 1100, 1500, 1800, 2100]
    headers = ["No.", "Description of Goods", "HS Code", "Qty", "Unit Price", "Amount"]
    
    for i, header in enumerate(headers):
        draw.text((cols[i], y), header, fill='black', font=font_bold)
    
    y += 50
    draw.line([(120, y), (width-120, y)], fill='black', width=1)
    
    # Table rows
    items = [
        ("1", "Laptop Computer 15.6 inch", "8471300000", "100 PCS", "USD 450.00", "USD 45,000.00"),
        ("2", "Wireless Mouse Optical", "8471600000", "500 PCS", "USD 12.00", "USD 6,000.00"),
        ("3", "USB-C Docking Station", "8473300000", "200 PCS", "USD 85.00", "USD 17,000.00"),
        ("4", "Mechanical Keyboard RGB", "8471607000", "300 PCS", "USD 35.00", "USD 10,500.00"),
        ("5", "Monitor LED 27 inch 4K", "8528520000", "50 PCS", "USD 320.00", "USD 16,000.00"),
        ("6", "Webcam HD 1080p", "8525801000", "200 PCS", "USD 28.00", "USD 5,600.00"),
        ("7", "External SSD 1TB", "8471700000", "150 PCS", "USD 65.00", "USD 9,750.00"),
        ("8", "Network Switch 24-port", "8517620000", "30 PCS", "USD 180.00", "USD 5,400.00"),
    ]
    
    for item in items:
        y += 15
        for i, val in enumerate(item):
            draw.text((cols[i], y), val, fill='black', font=font_small)
        y += 40
    
    # Total
    y += 20
    draw.line([(120, y), (width-120, y)], fill='black', width=2)
    y += 20
    draw.text((1100, y), "Total Quantity:", fill='black', font=font_bold)
    draw.text((1800, y), "1,530 PCS", fill='black', font=font_bold)
    y += 50
    draw.text((1100, y), "Gross Weight:", fill='black', font=font_bold)
    draw.text((1800, y), "4,250.00 KGS", fill='black', font=font_bold)
    y += 50
    draw.text((1100, y), "Net Weight:", fill='black', font=font_bold)
    draw.text((1800, y), "3,800.00 KGS", fill='black', font=font_bold)
    y += 50
    draw.text((1100, y), "Total Amount:", fill='black', font=font_bold)
    draw.text((1800, y), "USD 115,250.00", fill='black', font=font_bold)
    
    # Footer
    y += 100
    draw.line([(120, y), (width-120, y)], fill='gray', width=1)
    y += 30
    draw.text((120, y), "Terms of Payment: T/T 30 days after B/L date", fill='black', font=font_small)
    y += 40
    draw.text((120, y), "Terms of Delivery: CIF Jakarta, Indonesia (Incoterms 2020)", fill='black', font=font_small)
    y += 80
    draw.text((120, y), "Authorized Signature:", fill='gray', font=font_small)
    y += 50
    draw.text((120, y), "_________________________", fill='black', font=font_medium)
    y += 50
    draw.text((120, y), "Zhang Wei - Export Manager", fill='black', font=font_small)
    
    # Save
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, 'sample_invoice.png')
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ Sample invoice saved to: {output_path}")
    
    # Also save as lower quality to simulate scan
    img_scan = img.copy()
    img_scan = img_scan.resize((1240, 1754))  # Half resolution
    scan_path = os.path.join(output_dir, 'sample_invoice_scan.jpg')
    img_scan.save(scan_path, 'JPEG', quality=75)
    print(f"✅ Scanned version saved to: {scan_path}")
    
    return output_path


def create_sample_bl():
    """Create a sample Bill of Lading image"""
    
    width, height = 2480, 3508
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 52)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        font_bold = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_bold = ImageFont.load_default()

    # Border
    draw.rectangle([60, 60, width-60, height-60], outline='black', width=3)
    
    # Header
    y = 120
    draw.text((800, y), "BILL OF LADING", fill='black', font=font_large)
    y += 80
    draw.text((800, y), "ORIGINAL (3/3)", fill='gray', font=font_medium)
    
    # B/L Number
    draw.text((1600, 120), "B/L No: SHAJKT-2026-08815", fill='black', font=font_bold)
    
    y += 80
    draw.line([(120, y), (width-120, y)], fill='black', width=2)
    
    # Shipper
    y += 30
    draw.text((120, y), "Shipper:", fill='gray', font=font_small)
    y += 40
    draw.text((120, y), "SHANGHAI ELECTRONICS TRADING CO., LTD", fill='black', font=font_medium)
    y += 45
    draw.text((120, y), "No. 88 Pudong Avenue, Shanghai 200120, China", fill='black', font=font_small)
    
    # Consignee
    y += 80
    draw.line([(120, y), (width-120, y)], fill='gray', width=1)
    y += 20
    draw.text((120, y), "Consignee:", fill='gray', font=font_small)
    y += 40
    draw.text((120, y), "PT NUSANTARA TEKNOLOGI INDONESIA", fill='black', font=font_medium)
    y += 45
    draw.text((120, y), "Jl. Sudirman Kav. 52-53, Jakarta 12190, Indonesia", fill='black', font=font_small)
    
    # Notify Party
    y += 80
    draw.line([(120, y), (width-120, y)], fill='gray', width=1)
    y += 20
    draw.text((120, y), "Notify Party:", fill='gray', font=font_small)
    y += 40
    draw.text((120, y), "SAME AS CONSIGNEE", fill='black', font=font_medium)
    
    # Vessel & Voyage
    y += 80
    draw.line([(120, y), (width-120, y)], fill='black', width=2)
    y += 20
    
    # Two columns
    draw.text((120, y), "Ocean Vessel: MV EVER GOLDEN", fill='black', font=font_medium)
    draw.text((1200, y), "Voyage No: 0526E", fill='black', font=font_medium)
    y += 50
    draw.text((120, y), "Port of Loading: SHANGHAI, CHINA", fill='black', font=font_medium)
    draw.text((1200, y), "Port of Discharge: TANJUNG PRIOK, JAKARTA", fill='black', font=font_medium)
    y += 50
    draw.text((120, y), "Place of Delivery: TANJUNG PRIOK, JAKARTA, INDONESIA", fill='black', font=font_medium)
    
    # Cargo Details
    y += 80
    draw.line([(120, y), (width-120, y)], fill='black', width=2)
    y += 20
    
    cols = [120, 600, 1400, 1800, 2100]
    headers = ["Container No.", "Description", "Packages", "Gross Weight", "Measurement"]
    for i, h in enumerate(headers):
        draw.text((cols[i], y), h, fill='black', font=font_bold)
    
    y += 50
    draw.line([(120, y), (width-120, y)], fill='black', width=1)
    y += 20
    
    draw.text((120, y), "CSLU2345678", fill='black', font=font_medium)
    draw.text((600, y), "ELECTRONIC EQUIPMENT", fill='black', font=font_medium)
    draw.text((1400, y), "85 CTNS", fill='black', font=font_medium)
    draw.text((1800, y), "4,250 KGS", fill='black', font=font_medium)
    draw.text((2100, y), "28.5 CBM", fill='black', font=font_medium)
    
    y += 50
    draw.text((600, y), "SAID TO CONTAIN:", fill='gray', font=font_small)
    y += 35
    draw.text((600, y), "LAPTOP COMPUTERS, MONITORS,", fill='black', font=font_small)
    y += 35
    draw.text((600, y), "COMPUTER PERIPHERALS AND", fill='black', font=font_small)
    y += 35
    draw.text((600, y), "ACCESSORIES", fill='black', font=font_small)
    
    # Totals
    y += 80
    draw.line([(120, y), (width-120, y)], fill='black', width=2)
    y += 20
    draw.text((120, y), "Total Packages: 85 CARTONS", fill='black', font=font_bold)
    y += 50
    draw.text((120, y), "Total Gross Weight: 4,250.00 KGS", fill='black', font=font_bold)
    y += 50
    draw.text((120, y), "Total Measurement: 28.5 CBM", fill='black', font=font_bold)
    
    # Freight
    y += 80
    draw.text((120, y), "Freight: PREPAID", fill='black', font=font_medium)
    y += 50
    draw.text((120, y), "Number of Original B/L: THREE (3)", fill='black', font=font_medium)
    y += 50
    draw.text((120, y), "Place and Date of Issue: SHANGHAI, 16 MAY 2026", fill='black', font=font_medium)
    
    # Signature
    y += 100
    draw.text((1600, y), "Signed by:", fill='gray', font=font_small)
    y += 50
    draw.text((1600, y), "_____________________", fill='black', font=font_medium)
    y += 40
    draw.text((1600, y), "As Agent for the Carrier", fill='gray', font=font_small)
    
    # Save
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, 'sample_bill_of_lading.png')
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ Sample B/L saved to: {output_path}")
    
    return output_path


def create_sample_packing_list():
    """Create a sample Packing List image"""
    
    width, height = 2480, 3508
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 52)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        font_bold = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 52)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
            font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_bold = ImageFont.load_default()

    # Border
    draw.rectangle([60, 60, width-60, height-60], outline='black', width=3)
    
    # Header
    y = 120
    draw.text((900, y), "PACKING LIST", fill='black', font=font_large)
    y += 80
    draw.line([(120, y), (width-120, y)], fill='black', width=2)
    
    # Shipper
    y += 30
    draw.text((120, y), "Shipper / Exporter:", fill='gray', font=font_small)
    y += 40
    draw.text((120, y), "SHANGHAI ELECTRONICS TRADING CO., LTD", fill='black', font=font_medium)
    y += 45
    draw.text((120, y), "No. 88 Pudong Avenue, Shanghai 200120, China", fill='black', font=font_small)
    
    # Reference
    draw.text((1400, 230), "Ref. Invoice: INV-2026-00451", fill='black', font=font_medium)
    draw.text((1400, 280), "Date: 15/May/2026", fill='black', font=font_medium)
    
    # Consignee
    y += 80
    draw.line([(120, y), (width-120, y)], fill='gray', width=1)
    y += 20
    draw.text((120, y), "Consignee:", fill='gray', font=font_small)
    y += 40
    draw.text((120, y), "PT NUSANTARA TEKNOLOGI INDONESIA", fill='black', font=font_medium)
    y += 45
    draw.text((120, y), "Jl. Sudirman Kav. 52-53, Jakarta 12190, Indonesia", fill='black', font=font_small)
    
    # Marks & Numbers
    y += 80
    draw.line([(120, y), (width-120, y)], fill='gray', width=1)
    y += 20
    draw.text((120, y), "Marks & Numbers:", fill='gray', font=font_small)
    y += 40
    draw.text((120, y), "N/M - CSLU2345678", fill='black', font=font_medium)
    y += 45
    draw.text((120, y), "MADE IN CHINA", fill='black', font=font_medium)
    
    # Table Header
    y += 80
    draw.line([(120, y), (width-120, y)], fill='black', width=2)
    y += 15
    
    cols = [120, 350, 1000, 1400, 1700, 2000, 2250]
    headers = ["Ctn No.", "Description", "Qty/Ctn", "Net Wt (KG)", "Gross Wt (KG)", "Meas (CBM)", "Dims (cm)"]
    for i, h in enumerate(headers):
        draw.text((cols[i], y), h, fill='black', font=font_bold if i == 0 else font_small)
    
    y += 50
    draw.line([(120, y), (width-120, y)], fill='black', width=1)
    
    # Table rows
    items = [
        ("1-20", "Laptop Computer 15.6 inch", "5 PCS", "180.00", "210.00", "4.80", "60x40x50"),
        ("21-30", "Monitor LED 27 inch 4K", "5 PCS", "150.00", "175.00", "3.50", "70x50x40"),
        ("31-55", "Wireless Mouse + Keyboard", "32 PCS", "48.00", "56.00", "2.80", "50x40x35"),
        ("56-65", "USB-C Docking Station", "20 PCS", "60.00", "72.00", "2.40", "50x40x30"),
        ("66-75", "Webcam HD 1080p", "20 PCS", "24.00", "30.00", "1.50", "40x35x30"),
        ("76-80", "External SSD 1TB", "30 PCS", "15.00", "18.00", "0.90", "30x25x30"),
        ("81-85", "Network Switch 24-port", "6 PCS", "36.00", "42.00", "1.20", "40x35x25"),
    ]
    
    for item in items:
        y += 15
        for i, val in enumerate(item):
            draw.text((cols[i], y), val, fill='black', font=font_small)
        y += 40
    
    # Totals
    y += 30
    draw.line([(120, y), (width-120, y)], fill='black', width=2)
    y += 20
    draw.text((120, y), "Total Cartons: 85 CTNS", fill='black', font=font_bold)
    y += 50
    draw.text((120, y), "Total Quantity: 1,530 PCS", fill='black', font=font_bold)
    y += 50
    draw.text((120, y), "Total Net Weight: 3,800.00 KGS", fill='black', font=font_bold)
    y += 50
    draw.text((120, y), "Total Gross Weight: 4,250.00 KGS", fill='black', font=font_bold)
    y += 50
    draw.text((120, y), "Total Measurement: 28.50 CBM", fill='black', font=font_bold)
    
    # Footer
    y += 100
    draw.line([(120, y), (width-120, y)], fill='gray', width=1)
    y += 30
    draw.text((120, y), "Remarks: All goods packed in standard export cartons with foam protection.", fill='black', font=font_small)
    y += 40
    draw.text((120, y), "Each carton labeled with shipping marks, item description, and carton number.", fill='black', font=font_small)
    
    y += 100
    draw.text((120, y), "Prepared by:", fill='gray', font=font_small)
    y += 50
    draw.text((120, y), "_________________________", fill='black', font=font_medium)
    y += 50
    draw.text((120, y), "Li Ming - Warehouse Manager", fill='black', font=font_small)
    
    # Save
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, 'sample_packing_list.png')
    img.save(output_path, 'PNG', quality=95)
    print(f"\u2705 Sample Packing List saved to: {output_path}")
    
    return output_path


if __name__ == '__main__':
    print("Generating sample documents for demo...")
    print()
    create_sample_invoice()
    create_sample_bl()
    create_sample_packing_list()
    print()
    print("Done! Use these files to test the Smart Drafting Engine.")
