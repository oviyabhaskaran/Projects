import os
import json
import pandas as pd
import warnings
import yaml
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from functionality.document import read_json

# Filter out all warnings
warnings.filterwarnings("ignore")

def load_config(config_path):
    """
    Load configuration from a YAML file.

    Parameters:
        config_path (str): Path to the YAML configuration file.

    Returns:
        dict: Configuration dictionary loaded from the file.
    """
    with open(config_path) as f:
        config_json = yaml.safe_load(f)
    return config_json

def get_openai_api_key(config_json):
    """
    Retrieve the OpenAI API key from the configuration dictionary.

    Parameters:
        config_json (dict): Configuration dictionary containing OpenAI API key.

    Returns:
        str or None: OpenAI API key if found, None otherwise.
    """
    if 'openai' in config_json and 'api_key' in config_json['openai']:
        return config_json['openai']['api_key']
    else:
        return None

def summarize_company_performance(df, openai_api_key):
    """
    Summarize the performance of each company in the DataFrame and save the summaries as JSON files.

    Parameters:
        df (DataFrame): Input DataFrame containing company performance data.
        openai_api_key (str): API key for OpenAI API.

    Returns:
        None

    Example Summary JSON Format:
        {
          "Company Name": "Company 1 Performance Report",
          "Sales": "",
          "Operating Profit": "",
          "Net Profit": "",
          "PAT Margin": "",
          "Gross Profit Margin": "",
          "Operating Profit Margin": "",
          "Overall performance":""
        }

    Note:
        The function iterates through each unique company in the DataFrame, summarizes its performance using OpenAI, and saves the summary as a JSON file in the 'output_json' directory.
    """

    # excel_file_path = "Company_Performance_Report_langchain_Output.xlsx"
    # df = pd.read_excel(excel_file_path)

    unique_companies = df['Company Name'].unique()

    for company in unique_companies:
        company_df = df[df['Company Name'] == company]
        print("company_df")
        print(company_df)

        data = {
            "column_names": list(company_df.columns),
            "table_data": company_df.to_string(index=True)
        }
        # print(data)

        llm = OpenAI(openai_api_key=openai_api_key, temperature=0, max_tokens=2500)
        # print(llm)

        prompt_template = """As an expert data analyst, your task is to examine the provided company performance data, which is laid out in a table format. This table encompasses a variety of financial and operational metrics, potentially reported on a quarterly, monthly, or yearly basis. The metrics and their units are dynamic and may vary from one report to another.

Given the data:

{table_data}

Your goal is to generate a nuanced performance report. Analyze each metric provided, considering the time frames and units specific to the data. Your analysis should offer insights into trends(with respect to units), significant changes, and overall financial health, based on the available metrics.

Output your findings in a JSON format, adaptable to the metrics and time periods provided, like the example below:

{{
  "Company Name": "Company1 performance report",
    "Metric 1": "Insightful analysis based on its trend over the specified periods, covering values such as value1, value2, value3, value4 and so on if there.",
    "Metric 2": "Summary of performance, including any significant changes, with values like value1, value2, value3, value4 and so n=on if there.",
    "...": "Other metrics as per the data provided."
    "Dividend History": "Summary on company and metric wise all dividend history with dividend date"
    "Overall Summary": "A cohesive overview reflecting the company's performance, highlighting key trends and indicators derived from the analysis."
  
}}
Please ensure your analysis is flexible, catering to the specific metrics, units, and time periods in the supplied data. The aim is to provide clear, actionable insights, regardless of the data format.
"""

        prompt = PromptTemplate(
            input_variables=["column_names", "table_data"],
            template=prompt_template
        )

        chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
        summary = chain.run(data)
        json_file_name = f"{company}.json"

        # Define the directory name and the file name within that directory
        directory_name = "output_json"
        json_file_path = os.path.join(directory_name, json_file_name)


        # Create the directory if it doesn't exist
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        # Write JSON data to the file
        with open(json_file_path, 'w') as outfile:
            json.dump(summary, outfile)
    return directory_name


def convert_json_str_to_dict(input_directory, output_directory):
    # Create the directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate over all files in the input directory
    for filename in os.listdir(input_directory):
        input_file_path = os.path.join(input_directory, filename)
        read_json_file = read_json(input_file_path)

        # Convert string into dictionary
        dict_filename = json.loads(read_json_file)
        output_file_path = os.path.join(output_directory, filename)
   
        # Save the JSON data to the output file
        with open(output_file_path, "w") as output_file:
            json.dump(dict_filename, output_file)

    return output_directory
