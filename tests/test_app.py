import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Club" in data


def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Basketball Club"
    # Remove if already present
    client.delete(f"/activities/{activity}/participants/{email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200 or response.status_code == 400
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400


def test_remove_participant():
    activity = "Basketball Club"
    email = "removeme@mergington.edu"
    # Add participant first
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    # Try removing again
    response2 = client.delete(f"/activities/{activity}/participants/{email}")
    assert response2.status_code == 404


def test_root_redirect():
    response = client.get("/")
    assert response.status_code in (200, 307, 200)
