import pdfplumber
import pytesseract
from PIL import Image

def extract_text(file_path):
    """Extract text from a PDF or image file"""
    if file_path.lower().endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    else:
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)

# 👇 Change this line to your actual file path
file_path = "uploads/invoices/gulf-tech-invoice.pdf"

text = extract_text(file_path)
print("📄 Extracted text:")
print(text)
