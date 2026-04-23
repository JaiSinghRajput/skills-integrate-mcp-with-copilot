from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)
_original_activities = deepcopy(activities)


def setup_function():
    activities.clear()
    activities.update(deepcopy(_original_activities))


def test_signup_rejects_when_activity_is_full():
    activities["Chess Club"]["participants"] = [
        f"student{i}@mergington.edu" for i in range(activities["Chess Club"]["max_participants"])
    ]

    response = client.post(
        "/activities/Chess%20Club/signup?email=new-student@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_signup_allows_when_activity_has_space():
    response = client.post(
        "/activities/Chess%20Club/signup?email=new-student@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up new-student@mergington.edu for Chess Club"
    assert "new-student@mergington.edu" in activities["Chess Club"]["participants"]
