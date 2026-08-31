from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    initial_activities = client.get("/activities").json()
    assert email in initial_activities[activity_name]["participants"]

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    updated_activities = client.get("/activities").json()
    assert email not in updated_activities[activity_name]["participants"]

    # Restore in-memory state for future tests
    client.post(f"/activities/{activity_name}/signup?email={email}")
