## Invoice Processing Bot - Streamlit UI with Mistral AI

A smart invoice processing assistant that extracts, validates, and summarizes invoices using LLM agents, with Pymupdf for proper PDFs and built-in Mistral OCR for scanned or handwritten PDFs. Built with Streamlit UI and integrated with Mistral AI.

## Features

- **Auto PDF type detection** (embedded text vs scanned)
- **Extractor Agent** for structured JSON
- **Validator Agent** for high-value and missing GST check
- **Summary Agent** for 1-line result

## Streamlit UI

- Upload & progress display
- Raw OCR/PyMuPDF preview
- Extracted fields
- Final JSON + Summary
- Custom background image support

## Setup Instructions

1. Clone & Install

- git clone https://github.com/oviyabhaskaran/Invoice_Processing_Bot-Yavarai.git
- cd invoice-bot
- pip install -r requirements.txt

2. Add Your .env File

- MISTRAL_API_KEY=your_api_key_here

3. Run the App

- streamlit run streamlit_app.py

## Validations Applied

- **High Value** : if converted total > ₹1,00,000 (INR)
- **GST Missing** : if vendor GST not present or blank

## UI Layout

- Left Column: File Upload
- Center Column: Final Output + Summary
- Right Column: Raw OCR/Text + Extracted JSON
