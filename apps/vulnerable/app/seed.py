"""Reset the database to a known starting state: three users and three claims.

Run with: python -m app.seed
All data is synthetic. Running it again wipes and recreates everything.
"""

from decimal import Decimal

from app.db import Base, SessionLocal, engine
from app.models import Claim, User
from app.security import hash_password

# Synthetic lab users. The weak passwords are deliberate: they are part of the lesson.
SEED_USERS = [
    # (username, password, role, manager username)
    ("bob", "bob123", "manager", None),
    ("alice", "alice123", "employee", "bob"),
    ("carol", "carol123", "finance", None),
]


def seed() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        users: dict[str, User] = {}
        for username, password, role, manager in SEED_USERS:
            user = User(
                username=username,
                password_hash=hash_password(password),
                role=role,
                manager_id=users[manager].id if manager else None,
            )
            session.add(user)
            session.flush()  # assigns user.id now, so later users can reference it
            users[username] = user

        session.add_all([
            Claim(owner_id=users["alice"].id, amount=Decimal("42.50"),
                  description="Taxi to client office"),
            Claim(owner_id=users["alice"].id, amount=Decimal("640.00"),
                  description="Conference hotel, 2 nights",
                  status="approved", approved_by=users["bob"].id),
            Claim(owner_id=users["bob"].id, amount=Decimal("1899.00"),
                  description="New laptop"),
        ])
        session.commit()

    print("Seeded 3 users and 3 claims.")


if __name__ == "__main__":
    seed()
