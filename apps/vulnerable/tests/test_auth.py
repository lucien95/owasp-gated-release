"""Login works as intended. (These test the happy path; they do NOT test security.)"""

from tests.conftest import login


def test_login_with_correct_password_returns_a_token(client):
    token = login(client, "alice", "alice123")
    assert token.count(".") == 2  # a JWT has three dot-separated parts


def test_login_with_wrong_password_is_rejected(client):
    response = client.post("/auth/login", json={"username": "alice", "password": "wrong"})
    assert response.status_code == 401


def test_me_returns_the_logged_in_user(client):
    token = login(client, "alice", "alice123")
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.json() == {"id": 2, "username": "alice", "role": "employee"}


def test_request_without_token_is_rejected(client):
    assert client.get("/auth/me").status_code == 401
