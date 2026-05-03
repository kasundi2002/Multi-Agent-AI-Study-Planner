import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.difficulty_tool import analyze_difficulty_impl

def test_difficulty():
    topics = [
        "Introduction to Machine Learning",
        "Neural Networks"
    ]

    result = analyze_difficulty_impl(topics)

    assert isinstance(result, dict)
    assert result["Introduction to Machine Learning"] == "Easy"
    assert result["Neural Networks"] == "Hard"