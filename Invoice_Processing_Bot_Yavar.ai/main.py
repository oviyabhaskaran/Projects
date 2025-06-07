import pymupdf  
import base64
import json
import re
import os
from dotenv import load_dotenv
from mistralai import Mistral

# Setup Mistral API

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
model = "mistral-large-latest"
client = Mistral(api_key=api_key)

# Extract text from PDF

def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text.strip()

def extract_clean_json(text):
    # Remove triple backticks if they exist
    if text.strip().startswith("```json"):
        text = text.strip().removeprefix("```json").strip()
    elif text.strip().startswith("```"):
        text = text.strip().removeprefix("```").strip()

    # Remove ending backticks if present
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0].strip()

    # Ensure what's left starts with '{'
    json_start = text.find('{')
    if json_start == -1:
        raise ValueError("No JSON object found.")
    
    return text[json_start:]

# Extractor Agent using Mistral

def extractor_agent(raw_text):
    prompt = f"""
You are an invoice extraction assistant.

From the given invoice text, do the following:
1. Extract these fields and return a complete structured JSON:
   - invoice_number
   - invoice_date (YYYY-MM-DD)
   - vendor: name, address, gst_number
   - client: name, address, gst_number
   - total_amount:
      - currency (e.g. "USD", "INR", "EUR")
      - value (number only)
   - line_items: description, quantity, unit_price, net_worth, vat_percent, gross_worth
2. Do NOT perform currency conversion.
3. Line items may have multi-line descriptions. Join them unless a new quantity/price appears.
Return only a clean valid JSON. No explanation, no Markdown.
Here is the invoice text:
\"\"\"{raw_text}\"\"\"
"""

    response = client.chat.complete(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# Validator Agent using Mistral 

def validate_invoice(data):
    validations = []
    currency_rates = {
        "INR": 1.0,
        "USD": 85.28,
        "EUR": 90.11,
        "AED": 23.01,
        "MYR": 17.66
    }

    try:
        total = float(data["total_amount"]["value"])
        currency = data["total_amount"]["currency"].upper()
        inr_value = total * currency_rates.get(currency, 1.0)
        if inr_value > 100000:
            validations.append("High Value")

    except:
        validations.append("Invalid Total Amount")
    gst = data.get("vendor", {}).get("gst_number", "")

    if not gst or gst.lower() in ["", "null", "n/a"]:
        validations.append("GST Missing")

    data["validations"] = validations
    return data

# Summary Agent using Mistral

def summary_agent(data):
    validations = data.get("validations", [])
    if not validations:
        return "Invoice processed successfully with no validation issues."
    return f"Invoice flagged for: {', '.join(validations)}."

# Encode PDF as base64

def encode_pdf(pdf_path):

    try:
        with open(pdf_path, "rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding PDF: {e}")
        return None

# Fallback - Call Mistral OCR model if scanned or handwritten pdfs 

def run_mistral_ocr(base64_pdf):
    if not base64_pdf:
        return None

    try:
        response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": f"data:application/pdf;base64,{base64_pdf}"
            },
            include_image_base64=False
        )
        return response

    except Exception as e:
        print(f"Error calling Mistral OCR: {e}")
        return None

# Extract readable text from OCR JSON

def extract_text_from_ocr_response(response):
    if not response:
        return ""
    
    try:
        response_dict = response.model_dump()
        pages = response_dict.get("pages", [])
        # Mistral OCR stores raw content in `markdown`
        text_blocks = []
        for page in pages:
            markdown_text = page.get("markdown", "")
            if markdown_text:
                text_blocks.append(markdown_text)
        
        return "\n".join(text_blocks).strip()

    except Exception as e:
        print(f"Error extracting OCR text: {e}")
        return ""

# MAIN FLOW

if __name__ == "__main__":
    pdf_path = "handwritten_invoice.pdf"  
    raw_text = extract_text_from_pdf(pdf_path)
    print("raw_text is : ", raw_text)

    # If no text extracted using mistral model, then fallback to Mistral OCR

    if len(raw_text.strip()) < 20:  
        print("Pymupdf not extracted all fields, it might be scanned or handwritten pdf. Falling back to Mistral OCR")
        base64_pdf = encode_pdf(pdf_path)
        ocr_response = run_mistral_ocr(base64_pdf)
        #print("Raw Mistral OCR Response:")
        print(ocr_response.model_dump_json(indent=2))
        raw_text = extract_text_from_ocr_response(ocr_response)
        #print(f"Raw Text Extracted from PyMuPDF:\n{raw_text.strip()[:300]}...")

    if not raw_text.strip():
        print("Mistral OCR also failed to extract text. Skipping file.")
        exit()

    # Extract using LLM
    extracted_response = extractor_agent(raw_text)
    #print("extracted_response is : ", extracted_response)

    # Parse JSON 
    try:
        cleaned_json = extract_clean_json(extracted_response)
        structured_data = json.loads(cleaned_json)
    except Exception as e:
        print("Mistral returned invalid JSON.")
        print(extracted_response)
        print("Error:", e)
        exit()

    # Validation
    validated_data = validate_invoice(structured_data)

    # Summary
    validated_data["summary"] = summary_agent(validated_data)

    # Print Final Output
    print("\nFinal Output:")
    print(json.dumps(validated_data, indent=2))

# -----------------------------------------------


