import streamlit as st
import requests
import pandas as pd
import tempfile
from extractnet import Extractor
from transformers import pipeline
import tiktoken
import openai
import re
import json

# Setup OpenAI API key
openai.api_key = " "

# Setup TikToken encoding
encoding = tiktoken.get_encoding("cl100k_base")

# Setup zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0)


def process_and_classify_text(content, candidate_labels):
    paragraphs = [paragraph.strip() for paragraph in re.split(r'\n\s*', content) if paragraph]
    classification_results = []
    texts_classified_as_biography = []

    # Process each paragraph
    for paragraph in paragraphs:
        # Classify the paragraph
        classification = classifier(paragraph, candidate_labels)
        # Check if the 'biography' label is predicted for this text
        if classification['labels'][0] == 'biography':
            texts_classified_as_biography.append(paragraph)
        classification_results.append((paragraph, classification))

    return classification_results, texts_classified_as_biography


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def meta_pre1(raw_html):
    return {'first_value': 0}

def meta_pre2(raw_html):
    return {'first_value': 1, 'second_value': 2}

def find_stock_ticker(raw_html, results):
    matched_ticker = []
    for ticket in re.findall(r'[$][A-Za-z][\S]*', str(results['content'])):
      matched_ticker.append(ticket)
    return {'matched_ticker': matched_ticker}


# Cache the extract_content function
@st.cache_data
def extract_content(url):
    try:
        response = requests.get(url)
        print("URL Response:", response)
        if response.status_code == 404:
            raise Exception("Received a 404 error for URL:", url)

        raw_html = requests.get(url).text
        #print("Raw HTML:", raw_html)

        # Initialize Extractor with custom meta_preprocessing and postprocessing functions
        extract = Extractor(meta_postprocess=[meta_pre1, meta_pre2],
                            postprocess=[find_stock_ticker])

        results = extract(raw_html)
        #print("results:", results)
        content = results.get('content')
        #print("extractnet function side content")
        #print(content)
        #content = results.get('content')

        candidate_labels = ['biography', 'Terms and conditions']

        classification_results, texts_classified_as_biography = process_and_classify_text(content, candidate_labels)

        # Joins all the elements of the list into a single string
        content = ', '.join(texts_classified_as_biography)

        # content - zero shot classified biography content
        tokens_count = num_tokens_from_string(content, "cl100k_base")

        if tokens_count > 2600:  # adjust this threshold as per your needs
            raise Exception("Maximum content length is exceeded")

        return content

    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None


# Cache the openAI function
@st.cache_data
def openAI(content):
    try:
        chat = [{'role': 'system', 'content': 'Useful assistant'}]
        chat.append({'role': 'system', 'content': content})
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=chat)
        response = completion.choices[0].message.content
        return eval(response)
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None

output_1 = {'Prefix': 'Mrs', 'First Name': 'Patrice', 'Last Name': 'McCarty', 'Middle Name': 'Ann', 'Maiden Name': 'Williams', 'Gender': 'Female', 'Date of Birth': 'April 21, 1960', 'Date of Death': 'March 27, 2023', 'Age at Death': '62', 'Location City': 'Fennville', 'Location State': 'Michigan', 'Funeral Home': 'Chappell Funeral Home', 'Spouse Name': 'Rick McCarty', 'Education': 'degree in Nursing', 'Military Service': 'None mentioned', 'Spouse living status': 'Rick McCarty is still alive', 'Parents': 'George and Mary (Ke) Williams', 'Siblings': 'Ken (Linda) Williams and Dennis (Connie) Williams', 'Children': 'Shawna (Jose) Maciel and Cory Conklin', 'GrandChildren': 'Blake Walls, Lane Walls, Carlos Maciel, and Marcos Maciel', 'In-laws': 'None mentioned'}
output_2 = {'Prefix': 'Mrs', 'First Name': 'Iona', 'Last Name': 'Franklin', 'Middle Name': 'Louise', 'Maiden Name': 'Augustus', 'Gender': 'Female', 'Date of Birth': '1940', 'Date of Death': 'February 5, 2021', 'Age at Death': '80', 'Location City': 'Braithwaite', 'Location State': 'LA', 'Spouse name': 'Frank L. Franklin', 'Education': 'Phoenix High School', 'Military Service': '45 years of dedicated service in Juvenile Division', 'Spouse living status': 'Frank L. Franklin is still alive', 'Parents': 'Joseph Augustus and Laura Allen Kennetta', 'Siblings': 'None mentioned', 'Children': 'None mentioned', 'GrandChildren': 'Merwin and Fiona', 'In-laws': 'John and Mary Smith'}

def extract_attributes_openai(content, url):
    try:
        # few-shot prompting
        #print("Content:", content)
        prompt = f'''Input: Patrice Ann McCarty, 62 of Fennville, Michigan, passed away at her home on Tuesday, March 27, 2023. Born April 21, 1960, in Monroe, Michigan, she was the daughter of the late George and Mary (Keck) Williams and the wife of Rick McCarty. Together, as a family, they created many beautiful memories. She earned her bachelor’s degree in Nursing. Spending time with her children, grandchildren and great-grandchild added much joy to Patrice’s life. Along with her deep love of family, Patrice also adored her little Yorkshire terrier, Nikki. Patrice is survived by her husband, Rick; her children, Shawna (Jose) Maciel and Cory Conklin; four grandchildren, Blake Walls, Lane Walls, Carlos Maciel, and Marcos Maciel; one great-grandchild, Lexi Walls; and two siblings, Ken (Linda) Williams and Dennis (Connie) Williams. Visitation will be held at Chappell Funeral Home on Monday, April 3, 2023 from 11:00 AM to 12:00 PM, at which time the Funeral Service will begin at 12:00 PM, Pastor Brandon Beebe officiating. Patrice will be laid to rest in Plummerville Cemetery, Ganges Township, following the service.
        Output: {str(output_1)}
        Input: Iona Louise Augustus Franklin, Age 80 and a lifelong resident of Braithwaite, LA peacefully went to be with the Lord on Friday, February 5, 2021 at home with family. Born in 1940 to the late Joseph Augustus and Laura Allen in Braithwaite, Iona graduated from and retired after working 30 years at Phoenix High School. Beloved wife of Frank L. Franklin, Sr. Loving mother of Frank L. Franklin, Jr., Lional Franklin, Todd Franklin, Sr. and the late Kennetta Franklin Sylve. She lived with her In-laws, John and Mary Smith and grand children merwin and fiona. she retired after 45 years of dedicated service in Juvenile Division.
        Output: {str(output_2)}
        Input: {str(content)}
        Output: '''
        #print("Prompt:", prompt)
        response = openAI(prompt)
        response["Full_Obit_Text"] = content
        response["Obit_link"] = url
        return response
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None

# Streamlit app
def main():
        # Inject template CSS styles
    st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0.2rem;
        padding-right: 1rem;
    }

    [data-testid="stToolbar"] {
        background-color: rgba(0,0,0,0);
    }

    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }

    [data-testid="baseButton-header"] {
        background-color: rgba(0,0,0,0);
        display: none
    }

    [data-testid="stSidebar"] {
        background-image: url("https://images.pexels.com/photos/7130557/pexels-photo-7130557.jpeg");
        background-size: cover;
        max-height:fit-content;
        border-right-style: ridge;
    }

    [data-testid="stSidebarNavItems"] {
        padding-top: 0rem;
    }

    [data-testid="stSidebarNav"] {
        background-position: 20px 30px;
    }

    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/005/441/523/non_2x/abstract-white-and-gray-gradient-background-with-geometric-shape-illustration-vector.jpg");
        background-size: cover;
    }

    [data-testid="column"]:nth-child(1) {
        background-color: #fcfbf8;
        border-right-style: inset;
    }

    [data-testid="stBottomBlockContainer"] {
        background-color: rgba(0,0,0,0);
    }
    </style>
    """, unsafe_allow_html=True)

    # Add logo image with increased height using CSS
    st.sidebar.image("logo-black.png", use_column_width=False)
    
    st.title("Obituary Data Extraction")

    input_url = st.sidebar.text_input("Enter the input URL here")

    if st.sidebar.button("Generate"):
        if input_url:
            # Use the cached function to extract content
            content = extract_content(input_url)
            if content:
                # Use the cached function to extract attributes
                attributes = extract_attributes_openai(content, input_url)
                if attributes:
                    # Create DataFrame
                    df = pd.DataFrame.from_dict(attributes, orient='index').transpose()
                    # Display extracted attributes in Streamlit
                    st.write("Extracted Attributes:")
                    for key, value in attributes.items():
                        st.write(f"{key}: {value}")
                    json_data = json.dumps(attributes, indent=4)
                    # Download DataFrame as CSV file
                    csv = df.to_csv(index=True)
                    st.download_button(label="Download Extracted Attributes", data=csv,
                                       file_name="extracted_attributes.csv", mime="text/csv")
                else:
                    st.warning("No attributes extracted.")
            else:
                st.error("Failed to extract content from the provided URL.")
        else:
            st.warning("Please enter a valid URL.")


if __name__ == "__main__":
    main()
