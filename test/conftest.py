import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(scope="session")
def created_service(client):
    data = {"name": "Test Service", "description": "A service for testing"}
    response = client.post("/service", json=data)
    assert response.status_code == 200
    return response.json()
    