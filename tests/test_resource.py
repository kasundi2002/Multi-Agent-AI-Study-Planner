import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.resource_tool import get_resources_impl

def test_resources():
    topic = "Introduction to Machine Learning"
    resources = get_resources_impl(topic)

    assert isinstance(resources, list)
    assert len(resources) >= 1
    assert resources[0].startswith("http")