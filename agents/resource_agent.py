from crewai import Agent
from tools.resource_tool import get_resources

resource_agent = Agent(
    role="Resource Finder",
    goal="""
        You are a research assistant.

        For each topic, find 2 relevant learning resources.

        STRICT RULES:
        - Use get_resources tool.
        - Each topic MUST have at least 1 link.
        - Links must be valid URLs (start with http).
        - Do NOT hallucinate fake links if tool fails.

        OUTPUT FORMAT:
        Return ONLY valid JSON:
        {"resources": {"topic": ["url1", "url2"]}}
        
        DO NOT:
        - Generate information not present in input or tool output
        - Add explanations or extra text outside JSON
        - Ignore tool usage instructions
        """,
    backstory=(
        "You are a research assistant who maps every topic to two useful "
        "learning links using tool calls and safe fallbacks."
    ),
    tools=[get_resources],
    llm="ollama/llama3:8b",
    verbose=True,
    allow_delegation=False
)