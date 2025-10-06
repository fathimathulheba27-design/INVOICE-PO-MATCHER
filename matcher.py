import re

# === Step 1: Load files ===
with open("invoice.txt", "r") as f:
    invoice_text = f.read()

with open("po.txt", "r") as f:
    po_text = f.read()

# === Step 2: Extract Header Fields ===
def extract_header(text):
    header = {}
    lines = text.strip().splitlines()
    for line in lines:
        if ':' in line and not line.lower().startswith("item"):
            key, value = line.split(":", 1)
            header[key.strip()] = value.strip()
    return header

# === Step 3: Extract Items ===
def extract_items(text):
    item_pattern = re.compile(
        r"Item \d+:\s*(.*?)\s*Quantity:\s*(\d+)\s*Unit Price:\s*(\d+\.?\d*)\s*Total:\s*(\d+\.?\d*)",
        re.IGNORECASE | re.DOTALL
    )
    items = []
    for match in item_pattern.finditer(text):
        name, qty, price, total = match.groups()
        items.append({
            "name": name.strip(),
            "quantity": int(qty),
            "unit_price": float(price),
            "total": float(total)
        })
    return items

# === Step 4: Compare Items ===
def compare_items(invoice_items, po_items):
    mismatches = []

    if len(invoice_items) != len(po_items):
        mismatches.append(f"Item count mismatch: {len(invoice_items)} in invoice vs {len(po_items)} in PO.")
        return mismatches

    for i, (inv, po) in enumerate(zip(invoice_items, po_items), start=1):
        if inv['name'].lower() != po['name'].lower():
            mismatches.append(f"Item {i} name mismatch: {inv['name']} vs {po['name']}")
        if inv['quantity'] != po['quantity']:
            mismatches.append(f"Item {i} quantity mismatch: {inv['quantity']} vs {po['quantity']}")
        if inv['unit_price'] != po['unit_price']:
            mismatches.append(f"Item {i} unit price mismatch: {inv['unit_price']} vs {po['unit_price']}")
        if inv['total'] != po['total']:
            mismatches.append(f"Item {i} total mismatch: {inv['total']} vs {po['total']}")

    return mismatches

# === Step 5: Compare Headers ===
def compare_headers(invoice, po):
    mismatches = []
    if invoice.get("PO Number") != po.get("PO Number"):
        mismatches.append("PO Number mismatch.")
    if invoice.get("Vendor", "").lower() != po.get("Vendor", "").lower():
        mismatches.append("Vendor mismatch.")
    return mismatches

# === Step 6: Run ===
invoice_header = extract_header(invoice_text)
po_header = extract_header(po_text)
invoice_items = extract_items(invoice_text)
po_items = extract_items(po_text)

header_mismatches = compare_headers(invoice_header, po_header)
item_mismatches = compare_items(invoice_items, po_items)

# === Step 7: Report ===
print("\n=== Matching Result ===")
if not header_mismatches and not item_mismatches:
    print("✅ Invoice and PO match perfectly.")
else:
    print("❌ Mismatches found:")
    for issue in header_mismatches + item_mismatches:
        print("-", issue)

