import streamlit as st
import os

# Create folders if not exist
os.makedirs("uploads/invoices", exist_ok=True)
os.makedirs("uploads/pos", exist_ok=True)

# Upload Invoices
uploaded_invoices = st.file_uploader(
    "Upload up to 3 invoice files",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_invoices:
    for i, file in enumerate(uploaded_invoices[:3], start=1):
        save_path = os.path.join("uploads/invoices", file.name)
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())   # << saving file bytes
        st.success(f"✅ Invoice {i} saved: {file.name}")
        st.caption(f"Saved to: {save_path}")

# Upload Purchase Orders
uploaded_pos = st.file_uploader(
    "Upload up to 3 purchase order files",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_pos:
    for i, file in enumerate(uploaded_pos[:3], start=1):
        save_path = os.path.join("uploads/pos", file.name)
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())   # << saving file bytes
        st.success(f"✅ PO {i} saved: {file.name}")
        st.caption(f"Saved to: {save_path}")

