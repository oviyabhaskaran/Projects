import os
import streamlit as st
import zipfile
import logging
from functionality.process_input_file import process_input_excel_to_output
from functionality.generate_plots_file import generate_plots1, generate_plots2
from functionality.document import generate_company_report_document, read_json
from functionality.langchain_file import load_config, get_openai_api_key, summarize_company_performance, \
    convert_json_str_to_dict

# Function to empty a directory
def empty_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        os.remove(file_path)

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Streamlit app
def main():
    st.title("Company Performance Report Generation")

    # Upload Excel file
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

    if uploaded_file is not None:
        try:
            generate_button = st.button(label="Generate Company Report")

            if generate_button:
                # Call this function
                output_report_directory, output_plot_directory1, output_plot_directory2 = main2(uploaded_file)

                # Create a download button for all plot images as a zip file
                with zipfile.ZipFile("all_plots1.zip", "w") as zipf:
                    files = os.listdir(output_plot_directory1)
                    for file in files:
                        zipf.write(os.path.join(output_plot_directory1, file), arcname=file)

                with zipfile.ZipFile("all_plots2.zip", "w") as zipf:
                    files = os.listdir(output_plot_directory2)
                    for file in files:
                        zipf.write(os.path.join(output_plot_directory2, file), arcname=file)

                # Download button for the report document
                st.write("Download Company Report Document:")
                st.download_button(
                    label="Download Report",
                    data=open(os.path.join(output_report_directory, "Company_Performance_Report.docx"), "rb"),
                    file_name="Company_Performance_Report.docx"
                )
                st.success('Summarisation Completed successfully!')
        except Exception as e:
            # Log any errors that occur
            logging.error(f"An error occurred: {e}")
            st.error(f"An error occurred: {e}")

@st.cache_data
def main2(uploaded_file):
    # Log Excel file upload success
    logging.info("Company Performance Report Generation - Excel file uploaded successfully")

    # Create directories if they don't exist
    output_directories = ["output_json", "output_json_final", "output_plot_directory1", "output_plot_directory2"]
    for directory_name in output_directories:
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

    # Empty previous directory files
    empty_directory("output_json")
    empty_directory("output_json_final")
    empty_directory("output_plot_directory1")
    empty_directory("output_plot_directory2")

    # Read Excel file into DataFrame
    df, langchain_df = process_input_excel_to_output(input_excel_file=uploaded_file)

    # Log df calculation success
    logging.info("Company Performance Report Generation - DataFrame calculation done successfully")

    # Generate and display plots based on the condition of the 'Unit' column
    output_plot_directory1 = generate_plots1(df)
    output_plot_directory2 = generate_plots2(df)

    # Log plot generation success
    logging.info("Company Performance Report Generation - Plots generated successfully")

    # Here you can continue with the rest of your code, such as generating reports, etc.
    # Read Config - OpenAI Key
    config_path = 'configs/config.yaml'
    config_json = load_config(config_path)
    openai_api_key = get_openai_api_key(config_json)

    # LangChain - Summarize Company Performance
    json_directory = summarize_company_performance(df=langchain_df, openai_api_key=openai_api_key)

    # JSON File - Convert string into dictionary
    input_directory = "output_json"
    output_directory = "output_json_final"

    output_json_directory = convert_json_str_to_dict(input_directory, output_directory)

    # Log report json file creation success
    logging.info("Company Performance Report Generation - Json file created successfully")
    print("till plotting works")

    # Generate Company Performance Report
    output_report_directory = generate_company_report_document(json_directory=output_json_directory,
                                                           output_plot_directories=[output_plot_directory1, output_plot_directory2])
    
    # print("output_report_directory:", output_report_directory)
    print("generated")

    # Log report document generation success
    logging.info("Company Performance Report Generation - Company performance report generated successfully")
    print("completed")

    return output_report_directory, output_plot_directory1, output_plot_directory2

if __name__ == "__main__":
    main()

# streamlit run main.py
