import pdfplumber
import pytesseract
from PIL import Image

def extract_text(file_path):
    """Extract text from a PDF or image file"""
    # Case 1: If the file is a PDF
    if file_path.lower().endswith(".pdf"):
        text = "uploads/invoices/gulf-tech-invoice.pdf"
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:               # loop through all pages
                page_text = page.extract_text()  # extract text from page
                if page_text:                    # avoid None values
                    text += page_text + "\n"
        return text

    # Case 2: If the file is an image (JPG, PNG)
    else:
        img = Image.open(file_path)              # open the image
        text = pytesseract.image_to_string(img)  # OCR: extract text
        return text
