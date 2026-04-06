from pydantic import BaseModel
from typing import Optional


class ResearchRequest(BaseModel):
    """Request model for research endpoint."""
    company: str
    ticker: Optional[str] = None  # Optional: user can provide ticker directly


class ResearchResponse(BaseModel):
    """Response model for research endpoint."""
    report: str
    status: str = "completed"
    company: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str = "1.0.0"
