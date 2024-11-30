
#setting the openai key

import os
os.environ["OPENAI_API_KEY"] = ""

#neo4j database connection credentials

from langchain.graphs import Neo4jGraph

url = "bolt://localhost:"
username =""
password = ""

graph = Neo4jGraph(
    url=url,
    username=username,
    password=password
)

#defining the Cypher statement for finding the node as per user's query and extract the property which is stored as a prompt

from langchain.prompts.prompt import PromptTemplate
from langchain.chains import GraphCypherQAChain
from langchain.chat_models import ChatOpenAI

CYPHER_GENERATION_TEMPLATE = """Task: Generate Cypher query to retrieve the 'prompt' property of a node.
Instructions:
1. Use only the provided node label and property in the schema.
2. Do not use any other node labels or properties that are not provided.
3. Construct a Cypher query specifically designed to retrieve the 'prompt' property of a node.

Schema:
{schema}

Example Cypher Query:
# Retrieve the 'prompt' property of a PieChart node
MATCH (pc:PieChart)
RETURN pc.prompt

# Retrieve the 'prompt' property of an EDA node
MATCH (eda:EDA)
RETURN eda.prompt

Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

The question is:
{question}"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)


# Replace 'ChatOpenAI(temperature=0)' with your actual instantiation of the ChatOpenAI model
chain = GraphCypherQAChain.from_llm(
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'),
    graph=graph,
    verbose=True,
    return_direct=True,
    cypher_prompt=CYPHER_GENERATION_PROMPT,
)

result = chain.run("how to do eda?")

result

result = [{'bc.prompt': 'create a bar chart visualization with some sample values'}]

# Extract the prompt sentence
prompt_sentence = result[0]['bc.prompt']

prompt_sentence

import openai

# Set up your OpenAI API key
openai.api_key = ''

# Define the prompt
prompt = f"Code a Python script to {prompt_sentence}"

# Request code generation from the GPT-3.5-turbo model using the chat endpoint
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # GPT-3.5-turbo model
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ],
)

# Extract the generated code from the response
generated_code = response['choices'][0]['message']['content']

# Print or use the generated code as needed
print(generated_code)

