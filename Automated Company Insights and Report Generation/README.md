
# **Company Performance Report Generator**

A **Streamlit-based application** designed to automate the generation of detailed company performance reports. The application processes data from an uploaded Excel file, performs in-depth data analysis, generates visualizations, summarizes insights using GPT-powered LangChain, and produces a professional Word report.

---

## **Features**
- **Excel Data Analysis**:
  - Processes Excel files to extract key metrics and insights.
  - Calculates performance trends and generates analytical summaries.

- **Visualization**:
  - Creates multiple plot categories (e.g., `Unit`-based plots) to visualize company data trends.
  - Outputs plots into organized directories for further use.

- **GPT-Powered Summarization**:
  - Uses **LangChain** integrated with OpenAI GPT to provide concise, natural language summaries of company performance.
  - Converts raw data into actionable insights.

- **Report Generation**:
  - Produces a detailed Word document report that combines:
    - Summarized text.
    - Analytical plots.
  - Outputs reports in a format ready for stakeholders.

- **Streamlined User Interaction**:
  - Intuitive file upload and report generation via **Streamlit**.
  - One-click download buttons for:
    - The performance report.
    - Plot archives (as `.zip` files).

---

## **How It Works**
1. **Excel File Upload**:
   - Upload your Excel file via the app interface.
   
2. **Data Processing**:
   - The uploaded file is processed to generate key metrics and insights.
   - Output directories for JSON files and plots are created and cleaned dynamically.

3. **Visualization**:
   - Generates insightful plots to analyze company metrics.
   - Stores plots in designated directories.

4. **GPT-3 Integration**:
   - Summarizes the processed data into natural language insights using OpenAI GPT.

5. **Report Generation**:
   - Combines data, plots, and insights into a comprehensive Word document.

6. **Download**:
   - Download the final report and plots directly from the app.

---

## **Technologies Used**
- **Frontend**:
  - **[Streamlit](https://streamlit.io/):** For interactive user interface and seamless file uploads.

- **Backend**:
  - **[Python](https://www.python.org/):** Core programming language.
  - **[Pandas](https://pandas.pydata.org/):** For data manipulation and preprocessing.
  - **[Matplotlib](https://matplotlib.org/):** For data visualization.

- **AI Integration**:
  - **[LangChain](https://www.langchain.com/):** GPT-based summarization of company performance.
  - **[OpenAI GPT API](https://platform.openai.com/docs/):** Natural language generation.

- **Report Generation**:
  - **[python-docx](https://python-docx.readthedocs.io/):** To generate Word documents.

---

## **Directory Structure**
```
project-root/
├── main.py                   # Main Streamlit app
├── functionality/            # Helper modules
│   ├── process_input_file.py     # Processes Excel file
│   ├── generate_plots_file.py    # Generates plots
│   ├── document.py               # Creates Word reports and reads JSON
│   ├── langchain_file.py         # GPT-powered summarization logic
├── configs/                 # Configuration files (e.g., OpenAI API keys)
├── output_json/             # Intermediate JSON files
├── output_json_final/       # Processed JSON files
├── output_plot_directory1/  # Plots (category 1)
├── output_plot_directory2/  # Plots (category 2)
├── app.log                  # Log file for debugging
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## **Setup and Installation**

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install Dependencies**:
   Create a virtual environment and install required packages:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Add Configuration**:
   - Add your OpenAI API key in `configs/config.yaml`.

4. **Run the Application**:
   ```bash
   streamlit run main.py
   ```

---

## **Usage**
1. Launch the app and upload your Excel file.
2. Click the **Generate Company Report** button.
3. Download the:
   - Generated performance report.
   - Plot archives (`all_plots1.zip` and `all_plots2.zip`).

---

## **Sample Outputs**
- **Report**: A Word document summarizing key metrics and visualizing trends.
- **Plots**: `.png` files showcasing performance trends.

---

## **Logging and Debugging**
- Logs are stored in `app.log`.
- Errors and issues are displayed directly in the Streamlit interface.

---

## **Future Enhancements**
- Add support for additional data formats (e.g., CSV, JSON).
- Include dashboard-style visualization for real-time metrics.
- Leverage GPT-4 for enhanced summarization accuracy.

---
