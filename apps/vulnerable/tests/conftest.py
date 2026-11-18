"""Shared test setup: every test that asks for `client` starts from freshly seeded data."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.seed import seed


@pytest.fixture
def client():
    seed()
    return TestClient(app)


def login(client, username: str, password: str) -> str:
    response = client.post("/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["access_token"]
