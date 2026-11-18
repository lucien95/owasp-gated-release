"""The two tables: who the users are, and the claims they submit."""

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20))  # employee | manager | finance
    manager_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    description: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(20), default="submitted")  # submitted | approved | rejected | paid
    approved_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    paid_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
