import streamlit as st
import os
import json
from extractor import extract_text_from_file, extract_invoice_fields_from_text

# Folders for saving files
INVOICE_DIR = "uploads/invoices"
PO_DIR = "uploads/pos"
os.makedirs(INVOICE_DIR, exist_ok=True)
os.makedirs(PO_DIR, exist_ok=True)

st.title("📄 Invoice & PO Matcher")
st.header("Step 1: Upload Documents")

# Upload Invoices
invoices = st.file_uploader("Upload up to 3 Invoices", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
invoice_data = []

if invoices:
    st.subheader("📑 Extracted Invoice Data")
    for idx, file in enumerate(invoices, start=1):
        file_path = os.path.join(INVOICE_DIR, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        st.success(f"✅ Invoice {idx} uploaded & saved: {file.name}")

        try:
            text = extract_text_from_file(file_path)
            fields = extract_invoice_fields_from_text(text)
            invoice_data.append({"file": file.name, **fields})
            st.json(fields)
        except Exception as e:
            st.error(f"❌ Error processing {file.name}: {e}")

# Upload POs
pos = st.file_uploader("Upload up to 3 POs", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
po_data = []

if pos:
    st.subheader("📑 Extracted PO Data")
    for idx, file in enumerate(pos, start=1):
        file_path = os.path.join(PO_DIR, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        st.success(f"✅ PO {idx} uploaded & saved: {file.name}")

        try:
            text = extract_text_from_file(file_path)
            fields = extract_invoice_fields_from_text(text)  # reuse for PO
            po_data.append({"file": file.name, **fields})
            st.json(fields)
        except Exception as e:
            st.error(f"❌ Error processing {file.name}: {e}")

# Step 3: Compare Invoices & POs
from datetime import datetime

def parse_date_safe(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None

# Step 3: Compare Invoices & POs
if st.button("🔍 Compare Invoices & POs"):
    st.subheader("📊 Comparison Results")

    if not invoice_data or not po_data:
        st.warning("⚠️ Please upload both invoices and POs before comparing.")
    else:
        for inv in invoice_data:
            best_matches = []   # <-- collect all matches here
            for po in po_data:
                match_reasons = []

                # Rule: Subtotal match
                if "Subtotal" in inv and "Subtotal" in po:
                    if abs(float(inv["Subtotal"]) - float(po["Subtotal"])) < 1:
                        match_reasons.append("Subtotal")

                # Rule: Date match
                if inv.get("Invoice Date") == po.get("Invoice Date"):
                    match_reasons.append("Date")

                # ✅ Add other rules here later (Invoice Number, Vendor, etc.)

                if match_reasons:
                    best_matches.append((po, match_reasons))

            # ---- 👇 PLACE YOUR CODE HERE ----
            if best_matches:
                for po, match_reasons in best_matches:
                    st.success(
                        f"✅ Match: {inv['file']} ↔ {po['file']} "
                        f"(Matched on {', '.join(match_reasons)})"
                    )
            else:
                st.error(f"❌ No matching PO found for {inv['file']}")
