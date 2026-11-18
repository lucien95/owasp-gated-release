"""Login and access tokens. VULNERABLE: contains three planted flaws, marked below."""

import jwt
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.security import hash_password

router = APIRouter(prefix="/auth", tags=["auth"])

# PLANTED FLAW (A04:2025 Cryptographic Failures): the token-signing key is
# hard-coded in source code, and it is a guessable word. Anyone who reads this
# public repository, or guesses it, can sign their own valid tokens.
SECRET_KEY = "changeme"
ALGORITHM = "HS256"


class LoginRequest(BaseModel):
    username: str
    password: str


def create_token(user: User) -> str:
    # PLANTED FLAW (A07:2025 Authentication Failures): no "exp" (expiry) claim.
    # A token stolen today still works next year.
    claims = {"sub": str(user.id), "role": user.role}
    return jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)


def read_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        # PLANTED FLAW (A10:2025 Mishandling of Exceptional Conditions): when the
        # signature check FAILS, the code falls back to reading the token without
        # checking it ("fail open"). A forged token is therefore accepted.
        # Realistic origin: a quick workaround added while debugging, never removed.
        return jwt.decode(token, options={"verify_signature": False})


def get_current_user(
    authorization: str = Header(default=""),
    db: Session = Depends(get_db),
) -> User:
    """Turn the 'Authorization: Bearer <token>' header into the logged-in user."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    claims = read_token(authorization.removeprefix("Bearer "))
    user = db.get(User, int(claims["sub"]))
    if user is None:
        raise HTTPException(status_code=401, detail="Unknown user")
    return user


@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)) -> dict[str, str]:
    user = db.scalar(select(User).where(User.username == body.username))
    if user is None or user.password_hash != hash_password(body.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": create_token(user), "token_type": "bearer"}


@router.get("/me")
def me(user: User = Depends(get_current_user)) -> dict:
    """Who am I? Useful for checking which user a token really represents."""
    return {"id": user.id, "username": user.username, "role": user.role}
