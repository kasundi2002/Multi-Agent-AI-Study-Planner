from crewai import Agent
from tools.resource_tool import get_resources

resource_agent = Agent(
    role="Resource Finder",
    goal="Attach high quality resources to each structured topic",
    backstory=(
        "You are a research assistant who maps every topic to two useful "
        "learning links using tool calls and safe fallbacks."
    ),
    tools=[get_resources],
    llm="ollama/llama3:8b",
    verbose=True,
    allow_delegation=False
)