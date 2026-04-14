from hypothesis import given, strategies as st

from tools.scheduler_tool import create_schedule_impl


@given(
    topics=st.lists(
        st.text(
            alphabet=st.characters(whitelist_categories=("Ll", "Lu", "Nd", "Zs")),
            min_size=1,
            max_size=30,
        ),
        min_size=1,
        max_size=30,
        unique=True,
    ),
    days=st.integers(min_value=1, max_value=30),
)
def test_schedule_keeps_all_topics(topics: list[str], days: int) -> None:
    """Property: schedule should include each topic exactly once."""
    schedule = create_schedule_impl(topics=topics, days=days)
    flattened = [item for day_topics in schedule.values() for item in day_topics]
    assert sorted(flattened) == sorted(topics)
    assert len(flattened) == len(topics)


@given(
    topics=st.lists(st.text(min_size=1, max_size=20), min_size=1, max_size=20),
    days=st.integers(min_value=1, max_value=10),
)
def test_schedule_has_expected_day_keys(topics: list[str], days: int) -> None:
    """Property: schedule should create exactly N day buckets."""
    schedule = create_schedule_impl(topics=topics, days=days)
    assert len(schedule) == days
    assert all(key.startswith("Day ") for key in schedule.keys())
