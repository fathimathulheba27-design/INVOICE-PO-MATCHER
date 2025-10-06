import fitz  # PyMuPDF for PDF
from PIL import Image
import pytesseract

def extract_text_from_file(file_path: str) -> str:
    """Extract text from PDF or Image file"""
    text = ""

    if file_path.lower().endswith(".pdf"):
        # Use PyMuPDF for PDF
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()

    elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        # Use OCR for images
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

    else:
        raise ValueError("Unsupported file type")

    return text.strip()

import re
from decimal import Decimal
from datetime import datetime

def _to_decimal(value):
    try:
        return float(value.replace(",", "").replace("SAR", "").strip())
    except:
        return None

def _parse_date(value):
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date().isoformat()
    except:
        return None

def extract_invoice_fields_from_text(text: str):
    """Parse key invoice fields from text"""
    data = {}

    # Invoice Number
    match = re.search(r"Invoice\s*#[:\s]*([A-Za-z0-9\-]+)", text, re.IGNORECASE)
    if match:
        data["Invoice Number"] = match.group(1)

    # Invoice Date
    match = re.search(r"Date[:\s]*([0-9\-]{10})", text, re.IGNORECASE)
    if match:
        data["Invoice Date"] = _parse_date(match.group(1))

    # Due Date
    match = re.search(r"Due\s*Date[:\s]*([0-9\-]{10})", text, re.IGNORECASE)
    if match:
        data["Due Date"] = _parse_date(match.group(1))

    # Subtotal
    match = re.search(r"Subtotal[:\s]*([\d,\.]+)", text, re.IGNORECASE)
    if match:
        data["Subtotal"] = _to_decimal(match.group(1))

    # Total
    match = re.search(r"Total\s*Amount[:\s]*([\d,\.]+)", text, re.IGNORECASE)
    if match:
        data["Total"] = _to_decimal(match.group(1))

    return data   # ✅ always return a dict
