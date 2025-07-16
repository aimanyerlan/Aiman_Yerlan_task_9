def register_user(client, username, password):
    return client.post("/register", json={"username": username, "password": password})

def login_user(client, username, password):
    return client.post("/login", json={"username": username, "password": password})

def get_token(client, username, password):
    response = login_user(client, username, password)
    return response.json().get("access_token")

def test_register_success(client):
    response = register_user(client, "testuser", "testpass")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_register_duplicate(client):
    register_user(client, "duplicateuser", "pass")
    response = register_user(client, "duplicateuser", "pass")
    assert response.status_code == 400

def test_login_success(client):
    register_user(client, "logintest", "pass")
    response = login_user(client, "logintest", "pass")
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_fail(client):
    response = login_user(client, "wrong", "wrong")
    assert response.status_code == 401

def test_users_me_success(client):
    register_user(client, "meuser", "pass")
    token = get_token(client, "meuser", "pass")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "meuser"

def test_users_me_unauthorized(client):
    response = client.get("/users/me")
    assert response.status_code == 401 