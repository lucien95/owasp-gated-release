"""Approve, pay and import. Like the other tests, these check that things WORK, not that they are SAFE."""

import base64
import pickle

from tests.conftest import login


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_manager_approves_a_team_claim(client):
    token = login(client, "bob", "bob123")
    response = client.post("/claims/1/approve", headers=auth_header(token))
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
    assert response.json()["approved_by"] == 1


def test_employee_cannot_approve(client):
    token = login(client, "alice", "alice123")
    response = client.post("/claims/1/approve", headers=auth_header(token))
    assert response.status_code == 403


def test_finance_pays_an_approved_claim(client):
    token = login(client, "carol", "carol123")
    response = client.post("/claims/2/pay", headers=auth_header(token))
    assert response.status_code == 200
    assert response.json()["status"] == "paid"


def test_cannot_pay_a_claim_that_is_not_approved(client):
    token = login(client, "carol", "carol123")
    response = client.post("/claims/1/pay", headers=auth_header(token))
    assert response.status_code == 409


def test_finance_imports_claims_from_the_old_system(client):
    token = login(client, "carol", "carol123")
    export = [{"owner_id": 2, "amount": "15.00", "description": "Parking (imported)"}]
    data = base64.b64encode(pickle.dumps(export)).decode()
    response = client.post("/claims/import", json={"data": data}, headers=auth_header(token))
    assert response.status_code == 201
    assert response.json() == {"imported": 1}
