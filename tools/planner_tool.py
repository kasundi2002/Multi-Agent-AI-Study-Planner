from typing import List

from crewai.tools import tool


def load_topics_impl(subject: str) -> List[str]:
    """
    Return a curated topic list for a learning subject.

    Args:
        subject: User-provided subject name.

    Returns:
        Ordered list of topics. Returns a sensible default list when the subject is unknown.
    """
    normalized_subject = subject.strip().lower()
    topics_db = {
        "machine learning": [
            "Introduction to Machine Learning",
            "Python for ML",
            "Data Preprocessing",
            "Supervised Learning",
            "Regression",
            "Classification",
            "Model Evaluation",
            "Unsupervised Learning",
            "Neural Networks",
            "Mini Project",
        ],
        "artificial intelligence": [
            "Introduction to AI",
            "Problem Solving and Search",
            "Knowledge Representation",
            "Machine Learning Fundamentals",
            "Neural Networks",
            "Deep Learning",
            "Ethics in AI",
        ],
    }
    fallback_topics = [
        f"Introduction to {subject.title()}",
        "Core Concepts",
        "Hands-on Practice",
        "Intermediate Techniques",
        "Evaluation and Improvement",
    ]
    return topics_db.get(normalized_subject, fallback_topics)


@tool("load_topics")
def load_topics(subject: str) -> List[str]:
    """CrewAI tool wrapper for load_topics_impl."""
    return load_topics_impl(subject)