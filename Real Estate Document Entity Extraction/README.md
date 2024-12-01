
# Overview

The Real Estate Document Entity Extraction is a cutting-edge solution that automates the identification and extraction of critical building description entities from complex PDF documents. Leveraging advanced natural language processing (NLP) techniques and AI models, the system is designed to streamline the processing of real estate documents by efficiently retrieving and structuring essential information. This project integrates tools like **ChromaDB** for document storage, **LangChain** for seamless data access, and **GPT-3** for accurate and contextual entity recognition. 

## Key Features

- **Advanced Entity Recognition**  
  Utilizes GPT-3 to extract and identify key building attributes, including descriptions, locations, and dimensions, ensuring precise and reliable data retrieval.

- **Document Storage with ChromaDB**  
  Integrates ChromaDB with LangChain to enable efficient and secure document storage, ensuring seamless access and retrieval of PDF files.

- **OCR Integration**  
  Employs **EasyOCR** for text extraction from complex layouts, enhancing the accuracy of entity recognition from scanned and digital PDFs.

- **Data Preprocessing**  
  Applies preprocessing techniques such as punctuation removal, lemmatization, and stopword elimination to improve text analysis and model accuracy.

## How It Works

1. **PDF Parsing and Text Extraction**  
   Extracts raw text and layout data from PDFs using EasyOCR and LangChain document loaders.

2. **Entity Recognition**  
   Leverages GPT-3 to identify and extract entities such as building descriptions, addresses, and other key attributes.

3. **Text Preprocessing**  
   Cleans and prepares the extracted text for accurate analysis through advanced preprocessing steps.

4. **Document Storage and Retrieval**  
   Stores parsed documents securely in ChromaDB, enabling efficient retrieval and analysis.

5. **User Queries**  
   Uses LangChain and GPT-3 to process user queries, providing precise responses about document content, such as investment highlights or detailed property descriptions.

## Technologies Used

- **Python**: Core programming language.
- **EasyOCR**: For optical character recognition.
- **LangChain**: Framework for document retrieval and analysis.
- **ChromaDB**: Document storage solution.
- **GPT-3**: Model for entity recognition and contextual responses.
- **OpenCV**: Image processing for enhanced OCR results.
- **Tiktoken**: Tokenizer for handling large texts efficiently.
