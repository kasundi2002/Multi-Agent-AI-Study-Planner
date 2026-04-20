from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from main import run_pipeline
from state import StudyPlannerState


class PlanRequest(BaseModel):
    """HTTP request model for generating a study plan."""

    subject: str = Field(..., min_length=2, max_length=120)
    days: int = Field(..., ge=1, le=365)


app = FastAPI(title="Multi-Agent Study Planner API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    """Simple health endpoint for frontend and smoke checks."""
    return {"status": "ok"}


@app.post("/plan")
def create_plan(payload: PlanRequest) -> StudyPlannerState:
    """Generate a study plan using the existing local pipeline."""
    try:
        return run_pipeline(subject=payload.subject.strip(), days=payload.days)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
