from typing import Dict, List
from crewai.tools import tool

def analyze_difficulty_impl(topics: List[str]) -> Dict[str, str]:
    """Analyze the difficulty of a list of topics."""
    difficulty = {}
    for topic in topics:
        if "Introduction" in topic:
            difficulty[topic] = "Easy"
        elif "Neural" in topic or "Deep" in topic:
            difficulty[topic] = "Hard"
        else:
            difficulty[topic] = "Medium"
    return difficulty

@tool("analyze_difficulty")
def analyze_difficulty(topics: List[str]) -> Dict[str, str]:
    """CrewAI tool to analyze topic difficulty."""
    return analyze_difficulty_impl(topics)
