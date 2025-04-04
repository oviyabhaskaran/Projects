import requests
import xml.etree.ElementTree as ET

def fetch_research_papers(query, max_results=3):
    """
    Fetch relevant research papers from arXiv API based on a search query.

    Parameters:
        query (str): The search term for research papers.
        max_results (int): Number of research papers to fetch.

    Returns:
        list: A list of research paper dictionaries.
    """
    base_url = "http://export.arxiv.org/api/query"
    
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results
    }
    
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        root = ET.fromstring(response.text)
        papers = []
        
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            title = entry.find("{http://www.w3.org/2005/Atom}title").text
            summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
            link = entry.find("{http://www.w3.org/2005/Atom}id").text
            
            papers.append({"title": title, "summary": summary, "url": link})
        
        return papers
    else:
        print(f"Error fetching research papers: {response.status_code}, {response.text}")
        return []

# Example Usage
if __name__ == "__main__":
    papers = fetch_research_papers("climate change")
    for i, paper in enumerate(papers, start=1):
        print(f"{i}. {paper['title']} - {paper['url']}")

