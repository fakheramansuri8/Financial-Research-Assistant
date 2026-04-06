import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from crew.research_crew import create_research_crew
from api.schemas import ResearchRequest, ResearchResponse, HealthResponse

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Financial Research Assistant API",
    description="Multi-agent system for generating investment research reports",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok")


@app.post("/research", response_model=ResearchResponse)
async def run_research(request: ResearchRequest):
    """
    Generate an investment research report for a company.
    
    Args:
        request: ResearchRequest with company name and optional ticker
        
    Returns:
        ResearchResponse with generated report
        
    Raises:
        HTTPException: If API keys are not configured or research fails
    """
    # Validate API keys
    tavily_key = os.getenv("TAVILY_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not tavily_key or tavily_key == "your_tavily_api_key_here":
        raise HTTPException(
            status_code=500,
            detail="TAVILY_API_KEY not configured. Please set it in .env file."
        )
    
    if not gemini_key or gemini_key == "your_gemini_api_key_here":
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY not configured. Please set it in .env file."
        )
    
    try:
        # Create crew and execute research
        crew = create_research_crew()
        
        # Prepare inputs
        inputs = {"company": request.company}
        if request.ticker:
            inputs["ticker"] = request.ticker
        
        # Run the crew
        result = crew.kickoff(inputs=inputs)
        
        # Convert result to string (CrewAI returns CrewOutput object)
        report_text = str(result) if result else "No report generated."
        
        return ResearchResponse(
            report=report_text,
            status="completed",
            company=request.company
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Research failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
