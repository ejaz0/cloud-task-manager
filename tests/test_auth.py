from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_login_user(client: TestClient):
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "testpassword",
            "full_name": "Login User"
        },
    )
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "login@example.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
