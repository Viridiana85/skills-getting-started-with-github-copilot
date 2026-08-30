from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_delete_participant_from_activity():
    response = client.delete("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 200
    assert "michael@mergington.edu" not in response.json()["participants"]

    updated = client.get("/activities")
    assert "michael@mergington.edu" not in updated.json()["Chess Club"]["participants"]


def test_delete_missing_participant_returns_404():
    response = client.delete("/activities/Basketball Team/signup?email=missing@mergington.edu")

    assert response.status_code == 404
