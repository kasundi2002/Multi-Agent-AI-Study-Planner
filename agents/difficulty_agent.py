from crewai import Agent
from langchain_community.llms import Ollama
from tools.difficulty_tool import analyze_difficulty

# Using the user-provided setup
llm = Ollama(model="llama3:8b") # Match the model string from planner_agent to be safe if locally "llama3:8b" is pulled

difficulty_agent = Agent(
    role="Difficulty Analyzer",
    goal="""
        You are an academic difficulty analyzer.

        Classify each topic into one of:
        Easy, Medium, Hard.

        STRICT RULES:
        - Use analyze_difficulty tool.
        - Do NOT create new topics.
        - Each topic MUST have exactly one label.
        - Allowed labels ONLY: Easy, Medium, Hard.

        OUTPUT FORMAT:
        Return ONLY valid JSON:
        {"difficulties": {"topic1": "Easy", "topic2": "Hard"}}
        
        DO NOT:
        - Generate information not present in input or tool output
        - Add explanations or extra text outside JSON
        - Ignore tool usage instructions
        """,
    backstory="Expert curriculum analyst",
    tools=[analyze_difficulty],
    llm=llm,
    verbose=True,
    allow_delegation=False
)
