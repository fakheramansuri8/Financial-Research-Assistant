from crewai import Agent
from tools.finance_tool import FinancialDataTool
from config.llm_config import create_llm_instance


def create_financials_agent():
    """Create a financial data analyst agent."""
    return Agent(
        role="Financial Data Analyst",
        goal="Extract and summarize key financial metrics for {company}",
        backstory=(
            "You are a CFA charterholder specializing in fundamental analysis. "
            "You have deep expertise in interpreting financial statements, "
            "valuation metrics, and identifying red flags in company financials."
        ),
        tools=[FinancialDataTool()],
        llm=create_llm_instance(),
        verbose=True,
        allow_delegation=False
    )
