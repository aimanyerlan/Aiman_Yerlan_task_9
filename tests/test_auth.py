from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_success():
    response = client.post("/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_register_duplicate():
    client.post("/register", json={"username": "duplicateuser", "password": "pass"})
    response = client.post("/register", json={"username": "duplicateuser", "password": "pass"})
    assert response.status_code == 400

def test_login_success():
    client.post("/register", json={"username": "logintest", "password": "pass"})
    response = client.post("/login", json={"username": "logintest", "password": "pass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_fail():
    response = client.post("/login", json={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401
