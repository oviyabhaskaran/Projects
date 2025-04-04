import requests
from config import NEWSAPI_API_KEY  
from transformers import pipeline  

# Initialize the summarizer model (using Hugging Face's pre-trained model for summarization)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def fetch_news(query, num_articles=3):
    """
    Fetch latest news articles related to a given query using NewsAPI.

    Parameters:
        query (str): The search term for news.
        num_articles (int): Number of articles to fetch.

    Returns:
        list: A list of news article dictionaries.
    """
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize={num_articles}&apiKey={NEWSAPI_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        news_data = response.json()
        return news_data["articles"]  
    else:
        print(f"Error fetching news: {response.status_code}, {response.text}")
        return []


def summarize_article(article_text):
    """
    Summarize the article content using a pre-trained summarization model.

    Parameters:
        article_text (str): The text of the article to summarize.

    Returns:
        str: The summarized text.
    """
    if len(article_text) > 0:
        summary = summarizer(article_text, max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    else:
        return "No content available to summarize."


def get_news_with_summaries(query, num_articles=3):
    """
    Fetch news articles and summarize them.

    Parameters:
        query (str): The search term for news.
        num_articles (int): Number of articles to fetch and summarize.

    Returns:
        list: A list of dictionaries containing titles, sources, dates, summaries, and tags.
    """
    articles = fetch_news(query, num_articles)
    summarized_articles = []

    for article in articles:
        title = article.get("title", "No title available")
        source = article.get("source", {}).get("name", "Unknown")
        date = article.get("publishedAt", "Unknown Date")
        content = article.get("content", "No content available")

        # Summarize the content of the article
        summary = summarize_article(content)

        # Collect the structured article data
        summarized_articles.append({
            "title": title,
            "source": source,
            "date": date,
            "summary": summary,
            "tags": []  
        })

    return summarized_articles


# Example usage
if __name__ == "__main__":
    query = "climate change"  
    articles_with_summaries = get_news_with_summaries(query)

    for idx, article in enumerate(articles_with_summaries, start=1):
        print(f"{idx}. Title: {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   Date: {article['date']}")
        print(f"   Summary: {article['summary']}\n")
