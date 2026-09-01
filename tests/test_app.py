from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


# ============================================================================
# GET /activities tests
# ============================================================================


def test_get_activities_returns_all_activities():
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Track and Field",
        "Art Club",
        "Drama Club",
        "Debate Team",
        "Science Club",
    ]

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert set(data.keys()) == set(expected_activities)


def test_get_activities_includes_required_fields():
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in data.items():
        assert set(activity_data.keys()) == required_fields


# ============================================================================
# POST /activities/{activity_name}/signup tests
# ============================================================================


def test_signup_adds_participant_to_activity():
    # Arrange
    activity_name = "Basketball Team"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert "Signed up" in data["message"]
    assert email in data["message"]

    # Verify the participant was actually added
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_with_duplicate_email_returns_400():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up for Chess Club

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_to_nonexistent_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# ============================================================================
# DELETE /activities/{activity_name}/signup tests
# ============================================================================


def test_delete_participant_removes_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert email not in data["participants"]

    # Verify the participant was actually removed from the activity
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_delete_missing_participant_returns_404():
    # Arrange
    activity_name = "Basketball Team"
    email = "missing@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert "not signed up" in response.json()["detail"].lower()


def test_delete_from_nonexistent_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
