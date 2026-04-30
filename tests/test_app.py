import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert (AAA) pattern is used in all tests

def test_get_activities():
    # Arrange: (No setup needed, uses in-memory data)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "student1@example.com"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"


def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "student2@example.com"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Club"
    email = "student3@example.com"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_signup_success():
    # Arrange
    activity = "Programming Class"
    email = "student4@example.com"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"


def test_remove_signup_not_registered():
    # Arrange
    activity = "Programming Class"
    email = "student5@example.com"
    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not registered for this activity"


def test_remove_signup_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Club"
    email = "student6@example.com"
    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_root_redirect():
    # Arrange: (No setup needed)
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200 or response.status_code == 307  # Accept redirect or direct serve
    # If redirected, follow the redirect
    if response.is_redirect:
        redirected = client.get(response.headers["location"])
        assert redirected.status_code == 200
