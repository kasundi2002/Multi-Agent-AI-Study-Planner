from typing import List, Dict
from crewai.tools import tool

def generate_quiz_impl(topic: str) -> List[str]:
    """
    Generate quiz questions for a topic.
    """
    quiz_db = {
        "Introduction to AI": [
            "What is Artificial Intelligence?",
            "Name two AI applications",
            "What is Machine Learning?"
        ],
        "Neural Networks": [
            "What is a neuron?",
            "What is backpropagation?",
            "What is activation function?"
        ]
    }
    return quiz_db.get(topic, [f"What is {topic}?"])

@tool("generate_quiz")
def generate_quiz(topic: str) -> List[str]:
    """CrewAI tool to generate quiz questions for a topic."""
    return generate_quiz_impl(topic)
