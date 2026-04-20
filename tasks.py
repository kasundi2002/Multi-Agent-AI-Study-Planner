from crewai import Task
from agents.planner_agent import planner_agent
from agents.structurer_agent import structurer_agent
from agents.resource_agent import resource_agent
from agents.scheduler_agent import scheduler_agent
from agents.difficulty_agent import difficulty_agent
from agents.quiz_agent import quiz_agent

planner_task = Task(
    description=(
        "Input subject: {subject}. Generate only JSON with key `topics` "
        "containing a list of 8-12 learning topics. Use load_topics tool."
    ),
    expected_output='{"topics": ["..."]}',
    agent=planner_agent
)

structurer_task = Task(
    description=(
        "Read planner output and return only JSON with key "
        "`structured_topics` in beginner-to-advanced order. "
        "Use organize_topics tool."
    ),
    expected_output='{"structured_topics": ["..."]}',
    agent=structurer_agent,
    context=[planner_task]
)

resource_task = Task(
    description=(
        "For each topic from structurer output, call get_resources and "
        "return only JSON object with key `resources` "
        "as {topic: [link1, link2]}."
    ),
    expected_output='{"resources": {"topic": ["url1", "url2"]}}',
    agent=resource_agent,
    context=[structurer_task]
)

scheduler_task = Task(
    description=(
        "Using structured topics and user input days={days}, call "
        "create_schedule and return only JSON with key `schedule` as "
        "{'Day 1': ['topic']}. Then include key `save_path` after saving "
        "the final plan using save_plan."
    ),
    expected_output='{"schedule": {"Day 1": ["..."]}, "save_path": "path"}',
    agent=scheduler_agent,
    context=[resource_task]
)

difficulty_task = Task(
    description=(
        "Analyze the difficulty of the structured topics using analyze_difficulty tool. "
        "Return a JSON object with key `difficulties` containing {'topic': 'Easy/Medium/Hard'}."
    ),
    expected_output='{"difficulties": {"topic": "Easy"}}',
    agent=difficulty_agent,
    context=[structurer_task]
)

quiz_task = Task(
    description=(
        "For each structured topic, use the generate_quiz tool to generate quiz questions. "
        "Return a JSON object with key `quizzes` containing {'topic': ['Q1', 'Q2']}."
    ),
    expected_output='{"quizzes": {"topic": ["Q1"]}}',
    agent=quiz_agent,
    context=[structurer_task]
)