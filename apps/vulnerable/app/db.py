"""Database connection: one engine for the whole app, one session per unit of work."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://claims:local-dev-only@127.0.0.1:5432/claims",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Every table class inherits from this, so SQLAlchemy can find them all."""


def get_db():
    """Give each request its own database session, and always close it afterwards."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
