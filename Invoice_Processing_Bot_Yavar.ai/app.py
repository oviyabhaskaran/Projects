import streamlit as st
import tempfile
import json
import base64
import os
from pathlib import Path
from second_check import(
    extract_text_from_pdf, encode_pdf, run_mistral_ocr, extract_text_from_ocr_response,
    extractor_agent, extract_clean_json, validate_invoice, summary_agent
)

# UI Styling

st.set_page_config(page_title="Invoice Processing Bot", layout="wide")

# Set background image

def set_bg_from_local(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_bg_from_local("background.jpg") 

# Title
st.markdown("<h1 style='text-align: center; color: black;'>Invoice Processing Bot</h1>", unsafe_allow_html=True)
st.write("---")

# UI layout
col1, col2, col3 = st.columns([1, 1, 1])

# Left column - Upload

with col1:
    st.subheader("Upload PDF File")
    uploaded_file = st.file_uploader("Choose a invoice PDF", type=["pdf"])
    if uploaded_file:
        with st.spinner("Processing PDF..."):
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_path = tmp_file.name

            # Step 1: Try PyMuPDF
            raw_text = extract_text_from_pdf(temp_path)
            use_ocr = False

            if len(raw_text.strip()) < 20:
                use_ocr = True
                base64_pdf = encode_pdf(temp_path)
                ocr_response = run_mistral_ocr(base64_pdf)
                raw_text = extract_text_from_ocr_response(ocr_response)

# Right column - Raw source
with col3:
    if uploaded_file:
        if use_ocr:
            st.subheader("Scanned PDF / Handwritten PDF")
            st.markdown("**Mistral OCR Response:**")
            st.json(ocr_response.model_dump())
        else:
            st.subheader("Proper PDF")
            st.markdown("**Raw Text Extracted from PyMuPDF:**")
            st.text(raw_text[:500] + ("..." if len(raw_text) > 500 else ""))

        # Extract fields
        try:
            extracted_response = extractor_agent(raw_text)
            st.markdown("**Extracted Response from Mistral model:**")
            st.text(extracted_response)

            cleaned_json = extract_clean_json(extracted_response)
            structured_data = json.loads(cleaned_json)

            validated_data = validate_invoice(structured_data)
            validated_data["summary"] = summary_agent(validated_data)

        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

# Center column - Final output + Summary
with col2:
    if uploaded_file:
        st.subheader("Final Output")
        st.json(validated_data)

        st.markdown("### Summary")
        st.success(validated_data.get("summary", "No Summary available."))

        # Download button for final output
        st.markdown("### Download Output")
        json_data = json.dumps(validated_data, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name="invoice_output.json",
            mime="application/json"
        )