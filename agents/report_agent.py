from crewai import Agent
from config.llm_config import create_llm_instance


def create_report_agent():
    """Create a report writing agent."""
    return Agent(
        role="Investment Research Writer",
        goal="Write a professional, structured investment research report",
        backstory=(
            "You are a senior equity research analyst at a top-tier investment bank. "
            "You write clear, actionable research reports that institutional investors "
            "rely on for making investment decisions. Your reports are balanced, "
            "data-driven, and include specific recommendations."
        ),
        llm=create_llm_instance(),
        verbose=True,
        allow_delegation=False
    )
