🧾 Invoice Bot - Streamlit UI with Mistral AI
A smart invoice processing assistant that extracts, validates, and summarizes invoices using LLM agents, with built-in OCR fallback for scanned or handwritten PDFs. Built with Streamlit UI and integrated with Mistral AI.

📌 Features
🔍 Auto PDF type detection (embedded text vs scanned)

🧠 LLM-based Extractor Agent for structured JSON

✅ Validator Agent for high-value and missing GST checks

🧾 Summary Agent for 1-line results

📤 Streamlit UI with:

Upload & progress display

Raw OCR/PyMuPDF preview

Extracted fields

Final JSON + Summary

🖼️ Custom background image support

🔐 Secure .env API key loading

📁 Project Structure
css
Copy
Edit
project_folder/
├── .env                    ← API key (not pushed to GitHub)
├── .gitignore              ← hides .env
├── requirements.txt        ← all dependencies
├── streamlit_app.py        ← UI logic
├── your_invoice_script.py  ← invoice logic (agents, OCR)
├── background.png          ← optional UI background
⚙️ Setup Instructions
1. Clone & Install
bash
Copy
Edit
git clone https://github.com/yourusername/invoice-bot.git
cd invoice-bot
pip install -r requirements.txt
2. Add Your .env File
env
Copy
Edit
MISTRAL_API_KEY=your_api_key_here
⚠️ Do not commit this file

3. Run the App
bash
Copy
Edit
streamlit run streamlit_app.py
🔁 Agent Workflow Diagram
mermaid
Copy
Edit
graph TD
    A[Upload Invoice PDF] --> B{Extract text with PyMuPDF}
    B -- text found --> C[Send to Extractor Agent]
    B -- too short --> D[Call Mistral OCR]
    D --> E[Extract markdown text]
    E --> C
    C --> F[Validate with business rules]
    F --> G[Generate Summary]
    G --> H[Display in Streamlit UI]
✅ Validations Applied
High Value: if converted total > ₹1,00,000 (INR)

GST Missing: if vendor GST not present or blank

📷 UI Layout
Left Column: File Upload

Center Column: Final Output + Summary

Right Column: Raw OCR/Text + Extracted JSON

📃 License
MIT License © 2024 YourName

