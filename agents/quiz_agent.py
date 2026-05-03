from crewai import Agent
from langchain_community.llms import Ollama
from tools.quiz_tool import generate_quiz

llm = Ollama(model="llama3:8b") 

quiz_agent = Agent(
    role="Quiz Generator",
    goal="""
        You are an educational assessment generator.

        Generate 2–3 quiz questions per topic.

        STRICT RULES:
        - Use generate_quiz tool.
        - Questions must be clear and topic-specific.
        - Do NOT include answers.
        - Do NOT generate unrelated questions.

        OUTPUT FORMAT:
        Return ONLY valid JSON:
        {"quizzes": {"topic": ["Q1", "Q2"]}}
        
        DO NOT:
        - Generate information not present in input or tool output
        - Add explanations or extra text outside JSON
        - Ignore tool usage instructions
        """,
    backstory="Educational assessment expert",
    tools=[generate_quiz],
    llm=llm,
    verbose=True,
    allow_delegation=False
)
