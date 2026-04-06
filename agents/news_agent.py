from crewai import Agent
from tools.search_tool import NewsSearchTool
from config.llm_config import create_llm_instance


def create_news_agent():
    """Create a news research agent that fetches latest company news."""
    return Agent(
        role="Financial News Researcher",
        goal="Find the latest and most relevant news about {company}",
        backstory=(
            "You are an expert financial journalist with 10 years of experience "
            "covering equity markets. You excel at identifying material news "
            "that could impact stock prices and investor sentiment."
        ),
        tools=[NewsSearchTool()],
        llm=create_llm_instance(),
        verbose=True,
        allow_delegation=False
    )
