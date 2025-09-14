# 📘 Multimodal RAG for PDF Intelligence

An end-to-end **Multimodal Retrieval-Augmented Generation (RAG)** solution that extracts and embeds **text + images** from PDFs for intelligent document search and Q&A.  
This project combines **Vision Transformers (CLIP)** with **text embeddings**, indexed in **FAISS**, and connects the retriever with **GPT models** via **LangChain** for accurate multimodal reasoning.

---

## 🚀 Features
- Extracts **text** and **images** from PDFs using **PyMuPDF**.
- Generates **text embeddings** (for textual content).
- Generates **image embeddings** using **CLIP (OpenAI/ViT)**.
- Stores multimodal embeddings in **FAISS** for similarity search.
- Performs **multimodal retrieval** (text + image queries).
- Integrates with **GPT-4** via **LangChain** for context-aware answers.

---

## 🏗️ Architecture
1. **PDF Ingestion** → PyMuPDF extracts text + images.  
2. **Embedding Generation** → CLIP (for images), text embeddings (for text).  
3. **Vector Store** → FAISS indexes embeddings for fast retrieval.  
4. **Retriever** → Finds the most relevant chunks.  
5. **LLM (GPT-4)** → Generates final answer with retrieved context.  

![Flowchart](flowchart.png)  
*(Replace with actual image path once added)*

---

## 📂 Project Structure
```
multimodal-rag-pdf/
│── main.py               # Main pipeline script
│── utils/                # Helper functions
│── requirements.txt      # Python dependencies
│── README.md             # Project documentation
│── flowchart.png         # Architecture diagram
│── data/                 # Sample PDFs
```

---

## ⚙️ Installation
```bash
# Clone the repository
git clone https://github.com/<your-username>/multimodal-rag-pdf.git
cd multimodal-rag-pdf

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Usage
```bash
# Run the main script
python main.py --pdf data/sample.pdf --query "What is discussed in section 2?"
```

Example:
```
User Query: "What is the chart about in page 5?"
Answer: The chart shows the year-on-year revenue growth compared to industry benchmarks.
```

---

## 📦 Requirements
- Python 3.9+
- PyMuPDF
- FAISS
- OpenAI API / GPT-4
- LangChain
- Transformers (CLIP model)

Install with:
```bash
pip install -r requirements.txt
```

---

## 🔮 Future Improvements
- Add support for **multi-page image analysis**.
- Improve **chunking strategies** for long PDFs.
- Extend retrieval with **hybrid search (BM25 + FAISS)**.
- Deploy as a **Streamlit app** for interactive querying.

---

## 📜 License
MIT License. See [LICENSE](LICENSE) for details.

---

## 👩‍💻 Author
**Oviya Bhaskaran**  
📧 your-email@example.com  
🔗 [LinkedIn](https://linkedin.com/in/your-profile) | [GitHub](https://github.com/your-username)
