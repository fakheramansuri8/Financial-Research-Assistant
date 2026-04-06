import os
from dotenv import load_dotenv
from crewai.tools import BaseTool
from tavily import TavilyClient

load_dotenv()


class NewsSearchTool(BaseTool):
    name: str = "News Search"
    description: str = "Search for latest news about a company using Tavily API"

    def _run(self, query: str) -> str:
        """
        Search for news about a company.
        
        Args:
            query: Search query (company name or ticker)
            
        Returns:
            String containing news articles content
        """
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key or api_key == "your_tavily_api_key_here":
            return "Error: TAVILY_API_KEY not configured. Please set it in .env file."
        
        try:
            client = TavilyClient(api_key=api_key)
            result = client.search(
                query=query,
                search_depth="advanced",
                max_results=5
            )
            
            # Format results
            news_items = []
            for article in result.get('results', []):
                title = article.get('title', 'No title')
                content = article.get('content', 'No content')
                url = article.get('url', '')
                news_items.append(f"Title: {title}\nContent: {content}\nSource: {url}\n")
            
            return "\n".join(news_items) if news_items else "No news articles found."
            
        except Exception as e:
            return f"Error fetching news: {str(e)}"
