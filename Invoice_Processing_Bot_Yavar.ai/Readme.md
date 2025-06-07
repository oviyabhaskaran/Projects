## Invoice Processing Bot - Streamlit UI with Mistral AI

A smart invoice processing assistant that extracts, validates, and summarizes invoices using LLM agents, with Pymupdf for proper PDFs and built-in Mistral OCR for scanned or handwritten PDFs. Built with Streamlit UI and integrated with Mistral AI.

## Mistral AI

Mistral AI API provides a seamless way for developers to integrate Mistral's state-of-the-art models into their applications and production workflows with just a few lines of code. The Mistral models allows you to chat with a model that has been fine-tuned to follow instructions and respond to natural language prompts. A prompt is the input that you provide to the Mistral model. It can come in various forms, such as asking a question, giving an instruction, or providing a few examples of the task you want the model to perform. Based on the prompt, the Mistral model generates a text output as a response.

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

- streamlit run app.py

## Validations Applied

- **High Value** : if converted total > ₹1,00,000 (INR)
- **GST Missing** : if vendor GST not present or blank

## UI Layout

- Left Column: File Upload
- Center Column: Final Output + Summary
- Right Column: Raw OCR/Text + Extracted JSON

## Sources

- https://mistral.ai/products/la-plateforme
- https://pymupdf.readthedocs.io/en/latest/

## How can we proceed further

- Batch Processing
- Signature checking
- Google sheets

**Thank you for this Oppurtunity**. I have uploaded all the files regarding this task. I can explain elaborately in the meet if possible about how I came up with this solution and challenges faced. Looking Forward!
