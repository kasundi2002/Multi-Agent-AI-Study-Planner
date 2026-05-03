import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api import run_pipeline

def test_pipeline():
    subject = "Machine Learning"
    days = 5

    result = run_pipeline(subject, days)

    assert "topics" in result
    assert "structured_topics" in result
    assert "schedule" in result
    assert "resources" in result
    assert "quizzes" in result