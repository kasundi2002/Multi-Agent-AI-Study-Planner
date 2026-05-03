import json
from pathlib import Path
from typing import Dict, List

from crewai.tools import tool


def create_schedule_impl(topics: List[str], days: int) -> Dict[str, List[str]]:
    """
    Build a day-wise schedule that evenly distributes topics.

    Args:
        topics: Ordered learning topics.
        days: Number of learning days.

    Returns:
        Dictionary keyed by Day labels with list of topics per day.
    """
    normalized_days = max(1, int(days))
    schedule: Dict[str, List[str]] = {f"Day {i}": [] for i in range(1, normalized_days + 1)}
    for index, topic in enumerate(topics):
        day_idx = index % normalized_days + 1
        schedule[f"Day {day_idx}"].append(topic)
    return schedule


def save_plan_impl(plan: Dict[str, object], output_path: str = "study_plan.json") -> str:
    """
    Save the final study plan to a local JSON file.

    Args:
        plan: Final study plan dictionary.
        output_path: Path to save the generated plan.

    Returns:
        Absolute path to the saved file.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(plan, handle, indent=2, ensure_ascii=True)
    return str(path.resolve())


@tool("create_schedule")
def create_schedule(topics: List[str], days: int) -> Dict[str, List[str]]:
    """CrewAI tool wrapper for create_schedule_impl."""
    return create_schedule_impl(topics, days)


@tool("save_plan")
def save_plan(plan: Dict[str, object], output_path: str = "study_plan.json") -> str:
    """CrewAI tool wrapper for save_plan_impl."""
    return save_plan_impl(plan, output_path)