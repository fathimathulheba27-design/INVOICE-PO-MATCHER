import pdfplumber
import re

# Step 1: Extract text from PDF
file_path = "uploads/invoices/gulf-tech-invoice.pdf"  # 👈 change to your file path
text = ""
with pdfplumber.open(file_path) as pdf:
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

# Step 2: Parse important fields
def parse_invoice(text):
    data = {}

    # Invoice number
    match = re.search(r"Invoice #[:\s]*([A-Z0-9\-]+)", text)
    if match:
        data["Invoice Number"] = match.group(1)

    # Invoice date
    match = re.search(r"Date[:\s]*([0-9\-]+)", text)
    if match:
        data["Invoice Date"] = match.group(1)

    # Due date
    match = re.search(r"Due Date[:\s]*([0-9\-]+)", text)
    if match:
        data["Due Date"] = match.group(1)

    # Subtotal
    match = re.search(r"Subtotal:\s*([\d,.]+)", text)
    if match:
        data["Subtotal"] = float(match.group(1).replace(",", ""))

    # Total amount
    match = re.search(r"TOTAL AMOUNT\s*([\d,.]+)", text)
    if match:
        data["Total"] = float(match.group(1).replace(",", ""))

    return data

# Step 3: Run parser
parsed = parse_invoice(text)

print("📊 Parsed Invoice Data:")
print(parsed)
