import json
from typing import List
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import urlopen

from crewai.tools import tool


def get_resources_impl(topic: str) -> List[str]:
    """
    Get learning resources for a topic using hybrid retrieval.

    Hybrid strategy:
    1) Curated local resources (safe and deterministic).
    2) Free public API (Wikipedia REST summary endpoint).
    3) Fallback search suggestions.

    Args:
        topic: Learning topic string.

    Returns:
        List of resource URLs or useful fallback links.
    """
    curated_resources = {
        "Introduction to Machine Learning": [
            "https://www.coursera.org/learn/machine-learning",
            "https://developers.google.com/machine-learning/crash-course",
        ],
        "Supervised Learning": [
            "https://scikit-learn.org/stable/supervised_learning.html",
            "https://www.ibm.com/topics/supervised-learning",
        ],
        "Unsupervised Learning": [
            "https://scikit-learn.org/stable/unsupervised_learning.html",
            "https://www.ibm.com/topics/unsupervised-learning",
        ],
        "Neural Networks": [
            "https://www.deeplearning.ai/short-courses/",
            "https://www.ibm.com/topics/neural-networks",
        ],
    }
    if topic in curated_resources:
        return curated_resources[topic]

    wikipedia_url = _fetch_wikipedia_page(topic)
    if wikipedia_url:
        return [
            wikipedia_url,
            f"https://www.youtube.com/results?search_query={quote(topic + ' tutorial')}",
        ]

    return [
        f"https://www.google.com/search?q={quote(topic + ' learning resources')}",
        f"https://www.youtube.com/results?search_query={quote(topic + ' tutorial')}",
    ]


def _fetch_wikipedia_page(topic: str) -> str:
    """Return a Wikipedia page URL if the topic exists, otherwise empty string."""
    api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(topic)}"
    try:
        with urlopen(api_url, timeout=4) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return str(payload.get("content_urls", {}).get("desktop", {}).get("page", ""))
    except (URLError, TimeoutError, json.JSONDecodeError, OSError):
        return ""


@tool("get_resources")
def get_resources(topic: str) -> List[str]:
    """CrewAI tool wrapper for get_resources_impl."""
    return get_resources_impl(topic)