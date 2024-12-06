from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import List, Dict, Any
import logging
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone as LangchainPinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from pinecone import Pinecone, ServerlessSpec

# Set API key for OpenAI and Pinecone directly
os.environ['OPENAI_API_KEY'] = ''
os.environ['PINECONE_API_KEY'] = ''

# Initialize Pinecone
pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])

index_name = "test"
# Check if the index exists, if not, create it
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Set this to the appropriate dimension for your embeddings
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )

# Set OpenAI LLM and embeddings
llm_chat = ChatOpenAI(temperature=0.9, model='gpt-3.5-turbo')
embeddings = OpenAIEmbeddings()

# Set Pinecone index
docsearch = LangchainPinecone.from_existing_index(index_name=index_name, embedding=embeddings)

# Create chain
chain = load_qa_chain(llm_chat)

# FastAPI app
app = FastAPI()

class QueryRequest(BaseModel):
    question: str
    filenames: List[str]

class DocumentChunk(BaseModel):
    page_content: str
    metadata: Dict[str, Any]

class QueryResponse(BaseModel):
    answer: str
    relevant_chunks: List[DocumentChunk]

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    try:
        # Filter indexed documents by filenames directly in the search
        filter_criteria = {'source': {"$in": request.filenames}}
        
        # Perform similarity search with filter
        search_results = docsearch.similarity_search(request.question, filter=filter_criteria)
        
        # Logging the documents retrieved
        logging.info(f"Total documents retrieved: {len(search_results)}")
        
        if not search_results:
            logging.warning(f"No documents found for the given filenames: {request.filenames}")
            raise HTTPException(status_code=404, detail="No documents found for the given filenames.")

        response = chain.run(input_documents=search_results, question=request.question)

        # Format search results for response
        relevant_chunks = [DocumentChunk(page_content=doc.page_content, metadata=doc.metadata) for doc in search_results]

        return QueryResponse(answer=response, relevant_chunks=relevant_chunks)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=400, detail=f"An error occurred: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)