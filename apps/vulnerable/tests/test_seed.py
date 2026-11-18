"""Checks that the seed produces the starting state every later attack relies on."""

from sqlalchemy import func, select

from app.db import SessionLocal
from app.models import Claim, User
from app.seed import seed


def test_seed_creates_three_users_and_three_claims():
    seed()
    with SessionLocal() as session:
        assert session.scalar(select(func.count()).select_from(User)) == 3
        assert session.scalar(select(func.count()).select_from(Claim)) == 3


def test_alice_reports_to_bob():
    seed()
    with SessionLocal() as session:
        alice = session.scalar(select(User).where(User.username == "alice"))
        bob = session.scalar(select(User).where(User.username == "bob"))
        assert alice.manager_id == bob.id
