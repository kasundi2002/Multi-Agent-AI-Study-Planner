import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.planner_tool import load_topics_impl

def test_planner_topics():
    subject = "Machine Learning"
    topics = load_topics_impl(subject)

    assert isinstance(topics, list)
    assert len(topics) >= 5
    assert "Introduction to Machine Learning" in topics