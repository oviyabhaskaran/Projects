## Invoice Processing Bot - Streamlit UI with Mistral AI

A smart invoice processing assistant that extracts, validates, and summarizes invoices using LLM agents, with Pymupdf for proper PDFs and built-in Mistral OCR for scanned or handwritten PDFs. Built with Streamlit UI and integrated with Mistral AI.

## Features

- **Auto PDF type detection** (embedded text vs scanned)
- **LLM-based Extractor Agent** for structured JSON
- **Validator Agent** for high-value and missing GST checks
- **Summary Agent** for 1-line results

## Streamlit UI

- Upload & progress display
- Raw OCR/PyMuPDF preview
- Extracted fields
- Final JSON + Summary
- Custom background image support
- Secure .env API key loading

## Project Structure

project_folder/
├── .env                    ← Mistral AI API key 
├── requirements.txt        ← all dependencies
├── streamlit_app.py        ← UI logic
├── your_invoice_script.py  ← invoice logic (agents, OCR)
├── background.png          ← optional UI background

## Setup Instructions

1. Clone & Install

git clone https://github.com/yourusername/invoice-bot.git
cd invoice-bot
pip install -r requirements.txt

2. Add Your .env File

MISTRAL_API_KEY=your_api_key_here

3. Run the App

streamlit run streamlit_app.py

## Validations Applied

- **High Value** : if converted total > ₹1,00,000 (INR)
- **GST Missing** : if vendor GST not present or blank

## UI Layout

- Left Column: File Upload
- Center Column: Final Output + Summary
- Right Column: Raw OCR/Text + Extracted JSON
