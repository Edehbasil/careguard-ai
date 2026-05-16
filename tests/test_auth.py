from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_signup():
    response = client.post("/auth/signup", json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data


def test_signup_duplicate_email():
    client.post("/auth/signup", json={
        "email": "duplicate@example.com",
        "password": "testpassword"
    })
    response = client.post("/auth/signup", json={
        "email": "duplicate@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 400


def test_login():
    client.post("/auth/signup", json={
        "email": "logintest@example.com",
        "password": "testpassword"
    })
    response = client.post("/auth/login", data={
        "username": "logintest@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    client.post("/auth/signup", json={
        "email": "logintest@example.com",
        "password": "testpassword"
    })
    response = client.post("/auth/login", data={
        "username": "logintest@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_get_me_unauthenticated():
    response = client.get("/auth/users/me")
    assert response.status_code == 401