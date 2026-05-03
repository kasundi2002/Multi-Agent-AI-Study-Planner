import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.structurer_tool import organize_topics_impl

def test_structurer():
    topics = [
        "Neural Networks",
        "Introduction to Machine Learning",
        "Regression"
    ]

    structured = organize_topics_impl(topics)

    assert isinstance(structured, list)
    assert len(structured) == len(topics)
    assert structured[0] == "Introduction to Machine Learning"