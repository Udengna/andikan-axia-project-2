import pytest
from app import app
from utils import calculate_internal_metric


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# 1. Home endpoint returns 200
def test_home_status_code(client):
    response = client.get("/")
    assert response.status_code == 200


# 2. Home endpoint has correct message
def test_home_message(client):
    response = client.get("/")
    data = response.get_json()

    assert "message" in data
    assert data["message"] == "Internal Utility Service Running"


# 3. Environment field exists
def test_home_environment_present(client):
    response = client.get("/")
    data = response.get_json()

    assert "environment" in data


# 4. No sensitive data exposed in home endpoint
def test_home_no_sensitive_data(client):
    response = client.get("/")
    data = response.get_json()

    assert "db_host" not in data
    assert "db_user" not in data
    assert "db_password" not in data


# 5. Users endpoint returns 200
def test_users_status_code(client):
    response = client.get("/users")
    assert response.status_code == 200


# 6. Users endpoint returns a list
def test_users_returns_list(client):
    response = client.get("/users")
    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) > 0


# 7. Users do not expose secrets
def test_users_no_sensitive_data(client):
    response = client.get("/users")
    data = response.get_json()

    for user in data:
        assert "db_password" not in user
        assert "db_user" not in user


# 8. Health endpoint works correctly
def test_health_endpoint(client):
    response = client.get("/health")
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "healthy"


def test_metric_valid():
    assert calculate_internal_metric(10, 2) == 5


def test_metric_divide_by_zero():
    result = calculate_internal_metric(10, 0)
    assert result is None
