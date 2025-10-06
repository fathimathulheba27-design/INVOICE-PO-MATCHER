import os
import openai
import json

# Initialize OpenAI with your API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_invoice_po_fields(text):
    prompt = f"""
Extract the following fields from the text:  
- invoice_number  
- po_number  
- vendor  
- items (list with fields: name, quantity, unit_price, total)  
- total_amount

Return the result as a JSON object.

Text:
\"\"\"
{text}
\"\"\"
"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that extracts invoice and PO information."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )

    json_text = response.choices[0].message.content.strip()

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        data = {"error": "Failed to parse JSON", "raw_response": json_text}

    return data

# Quick test
if __name__ == "__main__":
    sample_text = """
Invoice Number: INV-1002
PO Number: PO-9001
Vendor: OfficeMart

Item 1: Pens
Quantity: 100
Unit Price: 1
Total: 100

Item 2: Notebooks
Quantity: 50
Unit Price: 2
Total: 100

Total Invoice Amount: 200
"""
    extracted = extract_invoice_po_fields(sample_text)
    print(json.dumps(extracted, indent=2))

