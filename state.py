from typing import Dict, List
from uuid import uuid4
from typing_extensions import TypedDict


class StudyPlannerState(TypedDict):
    """Canonical state contract shared across all agents."""

    user_goal: str
    days: int
    topics: List[str]
    structured_topics: List[str]
    resources: Dict[str, List[str]]
    schedule: Dict[str, List[str]]
    difficulties: Dict[str, str]
    quizzes: Dict[str, List[str]]
    final_plan_path: str
    trace_id: str


def create_initial_state(user_goal: str, days: int) -> StudyPlannerState:
    """Create the baseline state used by the sequential agent pipeline."""
    return {
        "user_goal": user_goal,
        "days": days,
        "topics": [],
        "structured_topics": [],
        "resources": {},
        "schedule": {},
        "difficulties": {},
        "quizzes": {},
        "final_plan_path": "",
        "trace_id": str(uuid4()),
    }