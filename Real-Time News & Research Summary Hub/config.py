import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
loaded = load_dotenv(dotenv_path)

print("Env Loaded:", loaded)  

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY") 
NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")

print("Loaded TAVILY_API_KEY:", repr(TAVILY_API_KEY))
print("Loaded NEWSAPI_API_KEY:", repr(NEWSAPI_API_KEY)) 