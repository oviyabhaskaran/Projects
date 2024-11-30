
## Overview
The Invoice Parsing System is a robust solution designed to automate the extraction of key entities from invoices with high accuracy. Leveraging the power of LayoutLMv3 and advanced preprocessing techniques, this system efficiently identifies and extracts critical details such as invoice numbers, dates, and totals. This system streamlines invoice processing, making it an invaluable tool for businesses seeking to optimize document management workflows.

## Key Features

- **Advanced Entity Recognition**: Developed an invoice parsing system utilizing LayoutLMv3 for precise row and entity recognition.
- **Training Data Annotation**: Used EasyOCR to annotate training samples by extracting text and layout structures from invoices.
- **Text Preprocessing**: Preprocessed data through techniques like punctuation removal, stopword removal, lemmatization, and stemming.
- **Model Training**: Trained LayoutLMv3 to identify critical entities such as invoice number, date, and total amount.
- **Real-Time Pipeline**: Designed a real-time invoice parsing pipeline with AWS S3 integration for secure file storage and retrieval.
- **Process Tracking**: Integrated Mobito API to enable status updates and process tracking during execution.
