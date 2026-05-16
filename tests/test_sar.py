from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_token(email="sartest@example.com", password="testpassword"):
    client.post("/auth/signup", json={"email": email, "password": password})
    response = client.post("/auth/login", data={"username": email, "password": password})
    return response.json()["access_token"]


def test_submit_sar():
    token = get_token()
    response = client.post("/sar/", json={
        "requester_name": "Test User",
        "requester_email": "testuser@example.com",
        "description": "Request for all personal data under UK GDPR Article 15"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"
    assert data["days_remaining"] is not None
    assert data["days_remaining"] <= 30


def test_submit_sar_unauthenticated():
    response = client.post("/sar/", json={
        "requester_name": "Test User",
        "requester_email": "testuser@example.com",
        "description": "Request for data"
    })
    assert response.status_code == 401


def test_list_sars():
    token = get_token("sarlist@example.com")
    client.post("/sar/", json={
        "requester_name": "Test User",
        "requester_email": "sarlist@example.com",
        "description": "Test SAR"
    }, headers={"Authorization": f"Bearer {token}"})
    response = client.get("/sar/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)