import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.scheduler_tool import create_schedule_impl

def test_scheduler():
    topics = [
        "Intro",
        "Regression",
        "Classification"
    ]

    schedule = create_schedule_impl(topics, 2)

    assert isinstance(schedule, dict)
    assert "Day 1" in schedule
    assert "Day 2" in schedule