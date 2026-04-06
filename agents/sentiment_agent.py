from crewai import Agent
from config.llm_config import create_llm_instance


def create_sentiment_agent():
    """Create a sentiment analysis agent."""
    return Agent(
        role="Sentiment Analyst",
        goal=(
            "Analyze the sentiment of news articles about {company} and provide "
            "a score from -1 (very negative) to +1 (very positive)"
        ),
        backstory=(
            "You are a behavioral finance expert skilled in NLP-based sentiment "
            "analysis. You understand how news sentiment correlates with market "
            "movements and can distinguish between noise and signal in media coverage."
        ),
        llm=create_llm_instance(),
        verbose=True,
        allow_delegation=False
    )
