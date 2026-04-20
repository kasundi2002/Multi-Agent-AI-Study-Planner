import json
from typing import Dict, List

from logger import log_event
from state import StudyPlannerState, create_initial_state
from tools.difficulty_tool import analyze_difficulty_impl
from tools.planner_tool import load_topics_impl
from tools.quiz_tool import generate_quiz_impl
from tools.resource_tool import get_resources_impl
from tools.scheduler_tool import create_schedule_impl, save_plan_impl
from tools.structurer_tool import organize_topics_impl


def run_pipeline(subject: str, days: int) -> StudyPlannerState:
    """Run the sequential 6-agent pipeline and return full global state."""
    state = create_initial_state(user_goal=subject, days=days)
    trace_id = state["trace_id"]

    # 1) Planner Agent owns state.topics
    log_event(agent="PlannerAgent", event_type="task_start", trace_id=trace_id, input_data={"subject": subject})
    log_event(
        agent="PlannerAgent",
        event_type="tool_call",
        trace_id=trace_id,
        tool_name="load_topics",
        tool_args={"subject": subject},
    )
    topics = load_topics_impl(subject=subject)
    state["topics"] = topics
    log_event(
        agent="PlannerAgent",
        event_type="task_end",
        trace_id=trace_id,
        output_data={"topics": topics},
        state_delta={"topics": topics},
    )

    # 2) Content Structurer Agent owns state.structured_topics
    log_event(
        agent="ContentStructurerAgent",
        event_type="task_start",
        trace_id=trace_id,
        input_data={"topics": topics},
    )
    log_event(
        agent="ContentStructurerAgent",
        event_type="tool_call",
        trace_id=trace_id,
        tool_name="organize_topics",
        tool_args={"topics_count": len(topics)},
    )
    structured_topics = organize_topics_impl(topics=topics)
    state["structured_topics"] = structured_topics
    log_event(
        agent="ContentStructurerAgent",
        event_type="task_end",
        trace_id=trace_id,
        output_data={"structured_topics": structured_topics},
        state_delta={"structured_topics": structured_topics},
    )

    # 3) Difficulty Analyzer Agent owns state.difficulties
    log_event(
        agent="DifficultyAnalyzerAgent",
        event_type="task_start",
        trace_id=trace_id,
        input_data={"structured_topics": structured_topics},
    )
    log_event(
        agent="DifficultyAnalyzerAgent",
        event_type="tool_call",
        trace_id=trace_id,
        tool_name="analyze_difficulty",
        tool_args={"topics_count": len(structured_topics)},
    )
    difficulties = analyze_difficulty_impl(topics=structured_topics)
    state["difficulties"] = difficulties
    log_event(
        agent="DifficultyAnalyzerAgent",
        event_type="task_end",
        trace_id=trace_id,
        output_data={"difficulties": difficulties},
        state_delta={"difficulties": difficulties},
    )

    # 4) Resource Finder Agent owns state.resources
    resources: Dict[str, List[str]] = {}
    log_event(
        agent="ResourceFinderAgent",
        event_type="task_start",
        trace_id=trace_id,
        input_data={"structured_topics_count": len(structured_topics)},
    )
    for topic in structured_topics:
        log_event(
            agent="ResourceFinderAgent",
            event_type="tool_call",
            trace_id=trace_id,
            tool_name="get_resources",
            tool_args={"topic": topic},
        )
        resources[topic] = get_resources_impl(topic=topic)
    state["resources"] = resources
    log_event(
        agent="ResourceFinderAgent",
        event_type="task_end",
        trace_id=trace_id,
        output_data={"resources_topics": list(resources.keys())},
        state_delta={"resources_count": len(resources)},
    )

    # 5) Scheduler Agent owns state.schedule
    log_event(
        agent="SchedulerAgent",
        event_type="task_start",
        trace_id=trace_id,
        input_data={"days": days, "structured_topics_count": len(structured_topics)},
    )
    log_event(
        agent="SchedulerAgent",
        event_type="tool_call",
        trace_id=trace_id,
        tool_name="create_schedule",
        tool_args={"days": days, "topics_count": len(structured_topics)},
    )
    schedule = create_schedule_impl(topics=structured_topics, days=days)
    state["schedule"] = schedule
    log_event(
        agent="SchedulerAgent",
        event_type="task_end",
        trace_id=trace_id,
        output_data={"schedule_days": len(schedule)},
        state_delta={"schedule": schedule},
    )

    # 6) Quiz Generator Agent owns state.quizzes
    quizzes: Dict[str, List[str]] = {}
    log_event(
        agent="QuizGeneratorAgent",
        event_type="task_start",
        trace_id=trace_id,
        input_data={"structured_topics_count": len(structured_topics)},
    )
    for topic in structured_topics:
        log_event(
            agent="QuizGeneratorAgent",
            event_type="tool_call",
            trace_id=trace_id,
            tool_name="generate_quiz",
            tool_args={"topic": topic},
        )
        quizzes[topic] = generate_quiz_impl(topic=topic)
    state["quizzes"] = quizzes
    log_event(
        agent="QuizGeneratorAgent",
        event_type="task_end",
        trace_id=trace_id,
        output_data={"quizzes_topics": list(quizzes.keys())},
        state_delta={"quizzes_count": len(quizzes)},
    )

    # Save final plan (includes all 6-agent outputs)
    final_plan = {
        "goal": state["user_goal"],
        "days": state["days"],
        "topics": state["topics"],
        "structured_topics": state["structured_topics"],
        "difficulties": state["difficulties"],
        "resources": state["resources"],
        "schedule": state["schedule"],
        "quizzes": state["quizzes"],
        "trace_id": state["trace_id"],
    }
    save_path = save_plan_impl(plan=final_plan, output_path="output/study_plan.json")
    state["final_plan_path"] = save_path
    log_event(
        agent="SchedulerAgent",
        event_type="task_end",
        trace_id=trace_id,
        output_data={"save_path": save_path},
        state_delta={"final_plan_path": save_path},
    )
    return state


def main() -> None:
    """CLI entry point for local execution."""
    subject = input("Enter subject: ").strip()
    days = int(input("Enter days: ").strip())
    print("\nStarting Multi-Agent Study Planner...\n")
    final_state = run_pipeline(subject=subject, days=days)
    print("FINAL OUTPUT:\n")
    print(json.dumps(final_state, indent=2))


if __name__ == "__main__":
    main()