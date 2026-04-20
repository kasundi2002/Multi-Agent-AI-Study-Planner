from fastapi.testclient import TestClient

from api import app


def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_plan_endpoint() -> None:
    client = TestClient(app)
    response = client.post("/plan", json={"subject": "Machine Learning", "days": 14})
    assert response.status_code == 200
    payload = response.json()
    assert "topics" in payload
    assert "structured_topics" in payload
    assert "resources" in payload
    assert "schedule" in payload
    assert "trace_id" in payload
