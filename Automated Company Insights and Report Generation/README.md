
# **Overview**

A Streamlit-based application designed to automate the generation of detailed company performance report. The application processes data from an uploaded Excel file, performs in-depth data analysis, generates visualizations, summarizes insights using GPT-powered LangChain, and produces a professional Word report.

## **Key Features**
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
env
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## **Sample Outputs**
- **Report**: A Word document summarizing key metrics and visualizing trends.
- **Plots**: `.png` files showcasing performance trends.
