
# InsightSnap: Real-Time News & Research Summary Hub

InsightSnap is an AI-powered application that fetches real-time news articles and research papers, and generates concise summaries. The tool aims to assist in gathering insights from various domains such as Climate Risk, InsureTech, and other topics relevant to the Insurance and Reinsurance businesses.

## Features
- Fetches news articles and research papers from NewsAPI and arXiv API.
- Summarizes articles and papers using Hugging Face's BART model.
- Outputs summarized results through a clean, easy-to-read report.
- Allows users to download the summary as a Word document (DOCX).

## Table of Contents
- [Installation](#installation)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)

## Installation
To run the application locally, follow these steps:

1. **Clone this repository:**

   ```bash
   git clone https://github.com/yourusername/insightsnap.git
   cd insightsnap
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables.** Create a `.env` file in the root directory with the following content:

   ```bash
   TAVILY_API_KEY=your_tavily_api_key
   GROQ_API_KEY=your_groq_api_key
   NEWSAPI_API_KEY=your_newsapi_api_key
   ```

5. **Install Hugging Face and other dependencies for transformers:**

   ```bash
   pip install transformers
   pip install streamlit
   pip install requests
   pip install python-dotenv
   pip install python-docx
   ```

## Setup Instructions

### API Keys:

You will need to obtain the API keys for NewsAPI, Tavily, and Groq. These keys should be set in your `.env` file to interact with their respective services.

You can sign up for these APIs at:
- [NewsAPI](https://newsapi.org/)
- [Groq API](https://groq.co/)
- [Tavily API](https://tavily.com/)

### Run the Application:

Start the Streamlit app:

```bash
streamlit run summarizer.py
```

## Access the Application:
The app will be available in your browser at `http://localhost:8501`.

## Usage
Once the application is running, users can:

- Enter a search query (e.g., "Climate change") into the input box.
- Click on the **Generate** button to fetch news articles and research papers related to the query.
- View summarized content displayed below the input area.
- Optionally, click the **Download Report** button to download the summarized content in a Word document format.
