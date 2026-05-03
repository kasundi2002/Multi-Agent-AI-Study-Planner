from typing import List

from crewai.tools import tool


def organize_topics_impl(topics: List[str]) -> List[str]:
    """
    Organize topics from foundational to advanced order.

    Args:
        topics: Unstructured topic list.

    Returns:
        Ordered topics prioritizing introductory concepts before advanced ones.
    """
    priority_keywords = [
        "introduction",
        "fundamentals",
        "python",
        "data",
        "supervised",
        "regression",
        "classification",
        "evaluation",
        "unsupervised",
        "neural",
        "deep",
        "project",
    ]

    def topic_score(topic: str) -> int:
        lowered = topic.lower()
        for index, keyword in enumerate(priority_keywords):
            if keyword in lowered:
                return index
        return len(priority_keywords) + 1

    return sorted(topics, key=lambda topic: (topic_score(topic), topic.lower()))


@tool("organize_topics")
def organize_topics(topics: List[str]) -> List[str]:
    """CrewAI tool wrapper for organize_topics_impl."""
    return organize_topics_impl(topics)