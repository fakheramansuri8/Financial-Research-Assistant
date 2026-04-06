from crewai import Crew, Task, Process
from agents.news_agent import create_news_agent
from agents.financials_agent import create_financials_agent
from agents.sentiment_agent import create_sentiment_agent
from agents.report_agent import create_report_agent


def create_research_crew():
    """
    Create and configure the research crew with all agents and tasks.
    
    Returns:
        Crew: Configured CrewAI instance ready to execute research tasks
    """
    # Create agents
    news_agent = create_news_agent()
    financials_agent = create_financials_agent()
    sentiment_agent = create_sentiment_agent()
    report_agent = create_report_agent()
    
    # Define tasks in sequential order
    tasks = [
        Task(
            description=(
                "Search for the latest news about {company} from the past 7 days. "
                "Focus on material events, earnings announcements, regulatory filings, "
                "and market-moving news."
            ),
            expected_output=(
                "A concise summary of the 5 most important news items with dates "
                "and sources. Highlight any material events that could impact the stock price."
            ),
            agent=news_agent
        ),
        Task(
            description=(
                "Retrieve key financial metrics for {company}. "
                "If a ticker symbol is not provided, infer it from the company name. "
                "Focus on valuation metrics, profitability, and growth indicators."
            ),
            expected_output=(
                "A structured summary of financial health indicators including "
                "valuation multiples, profitability metrics, and key ratios."
            ),
            agent=financials_agent
        ),
        Task(
            description=(
                "Analyze the sentiment of the news collected about {company}. "
                "Consider the tone, urgency, and potential market impact of each article. "
                "Provide an overall sentiment score and justify your assessment."
            ),
            expected_output=(
                "A sentiment score from -1 (very negative) to +1 (very positive) "
                "with detailed justification. Explain key drivers of sentiment."
            ),
            agent=sentiment_agent
        ),
        Task(
            description=(
                "Write a comprehensive investment research report for {company} "
                "that synthesizes all previous findings. The report must include:\n\n"
                "1. **Executive Summary** - Brief overview and key takeaways\n"
                "2. **Recent News Highlights** - Material developments\n"
                "3. **Financial Health Analysis** - Key metrics and trends\n"
                "4. **Sentiment Analysis** - Market perception and mood\n"
                "5. **Investment Recommendation** - Clear Buy/Hold/Sell rating with rationale\n"
                "6. **Key Risks** - Potential downside factors\n"
                "7. **Catalysts** - Near-term events that could move the stock\n\n"
                "Use professional language suitable for institutional investors."
            ),
            expected_output=(
                "A professional markdown-formatted investment research report "
                "(800-1200 words) with clear sections, actionable insights, "
                "and a definitive investment recommendation."
            ),
            agent=report_agent
        )
    ]
    
    # Create crew with sequential processing
    crew = Crew(
        agents=[news_agent, financials_agent, sentiment_agent, report_agent],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        memory=False  # Enable if you want to use ChromaDB memory
    )
    
    return crew
