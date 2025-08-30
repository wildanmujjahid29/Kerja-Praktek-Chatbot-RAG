import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_create_service():
    global service_id
    data = {"name": "Test Service", "description": "A service for testing"}
    response = client.post("/service", json=data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == data["name"]
    assert response_data["description"] == data["description"]
    assert "id" in response_data
    service_id = response_data["id"]

def test_list_service():
    response = client.get("/service")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
def test_get_service_by_id():
    global service_id
    if not service_id:
        test_create_service()
    response = client.get(f"/service/{service_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == service_id
    
def test_update_service():
    global service_id
    if not service_id:
        test_create_service()
    update_data = {"name" : "Updated Service", "description": "Updated description"}
    response = client.put(f"/service/{service_id}", json=update_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == update_data["name"]
    assert response_data["description"] == update_data["description"]
    
def test_delete_service():
    global service_id
    if not service_id:
        test_create_service()
    response = client.delete(f"/service/{service_id}")
    assert response.status_code == 200
