"""Claims tests. Like the auth tests, these check that things WORK, not that they are SAFE."""

from tests.conftest import login


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_submit_claim_belongs_to_the_submitter(client):
    token = login(client, "alice", "alice123")
    response = client.post(
        "/claims", json={"amount": "18.20", "description": "Lunch with client"}, headers=auth_header(token)
    )
    assert response.status_code == 201
    assert response.json()["owner_id"] == 2
    assert response.json()["status"] == "submitted"


def test_list_returns_only_my_claims(client):
    token = login(client, "alice", "alice123")
    response = client.get("/claims", headers=auth_header(token))
    assert response.status_code == 200
    assert [claim["id"] for claim in response.json()] == [1, 2]


def test_list_filters_by_status(client):
    token = login(client, "alice", "alice123")
    response = client.get("/claims", params={"status": "approved"}, headers=auth_header(token))
    assert [claim["id"] for claim in response.json()] == [2]


def test_view_my_own_claim(client):
    token = login(client, "alice", "alice123")
    response = client.get("/claims/1", headers=auth_header(token))
    assert response.status_code == 200
    assert response.json()["description"].lower().startswith("taxi")
