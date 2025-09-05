def test_create_service(created_service):
    assert "id" in created_service
    assert created_service["name"] == "Test Service"

