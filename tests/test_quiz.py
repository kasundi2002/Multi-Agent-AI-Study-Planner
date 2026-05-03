import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.quiz_tool import generate_quiz_impl

def test_quiz():
    topic = "Neural Networks"
    quiz = generate_quiz_impl(topic)

    assert isinstance(quiz, list)
    assert len(quiz) >= 1