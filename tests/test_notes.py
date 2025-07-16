def register_and_login(client, username, password):
    client.post("/register", json={"username": username, "password": password})
    response = client.post("/login", json={"username": username, "password": password})
    return response.json()["access_token"]

def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

def test_create_note(client):
    token = register_and_login(client, "noteuser", "pass")
    response = client.post("/notes", json={"text": "my note"}, headers=auth_headers(token))
    assert response.status_code == 200
    assert response.json()["text"] == "my note"

def test_get_notes_only_own(client):
    token1 = register_and_login(client, "user1", "pass")
    token2 = register_and_login(client, "user2", "pass")
    client.post("/notes", json={"text": "note1"}, headers=auth_headers(token1))
    client.post("/notes", json={"text": "note2"}, headers=auth_headers(token1))
    client.post("/notes", json={"text": "note3"}, headers=auth_headers(token2))
    response = client.get("/notes", headers=auth_headers(token1))
    notes = response.json()
    assert len(notes) == 2
    assert all(note["text"] in ["note1", "note2"] for note in notes)
    response = client.get("/notes", headers=auth_headers(token2))
    notes = response.json()
    assert len(notes) == 1
    assert notes[0]["text"] == "note3"

def test_delete_own_and_foreign_note(client):
    token1 = register_and_login(client, "owner", "pass")
    token2 = register_and_login(client, "intruder", "pass")
    response = client.post("/notes", json={"text": "secret"}, headers=auth_headers(token1))
    note_id = response.json()["id"]
    del_response = client.delete(f"/notes/{note_id}", headers=auth_headers(token1))
    assert del_response.status_code == 200
    response = client.post("/notes", json={"text": "another"}, headers=auth_headers(token1))
    note_id2 = response.json()["id"]
    del_response2 = client.delete(f"/notes/{note_id2}", headers=auth_headers(token2))
    assert del_response2.status_code == 404 or del_response2.status_code == 403 