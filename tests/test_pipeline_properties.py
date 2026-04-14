from main import run_pipeline


def test_pipeline_state_contract() -> None:
    """Pipeline should populate every required global-state field."""
    state = run_pipeline(subject="Machine Learning", days=14)
    required_keys = {
        "user_goal",
        "days",
        "topics",
        "structured_topics",
        "resources",
        "schedule",
        "final_plan_path",
        "trace_id",
    }
    assert required_keys.issubset(state.keys())
    assert state["user_goal"] == "Machine Learning"
    assert state["days"] == 14
    assert isinstance(state["trace_id"], str) and len(state["trace_id"]) > 10


def test_no_topic_loss_in_state() -> None:
    """Every structured topic should remain present in resources and schedule."""
    state = run_pipeline(subject="Machine Learning", days=10)
    structured = state["structured_topics"]
    resources = state["resources"]
    scheduled_topics = [topic for day_topics in state["schedule"].values() for topic in day_topics]

    for topic in structured:
        assert topic in resources
        assert len(resources[topic]) >= 1
        assert topic in scheduled_topics
