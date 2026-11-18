"""Claims: submit a claim, list your claims, view one claim. VULNERABLE on purpose."""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.db import get_db
from app.models import Claim, User

router = APIRouter(prefix="/claims", tags=["claims"])


class ClaimRequest(BaseModel):
    amount: Decimal
    description: str


def to_dict(claim: Claim) -> dict:
    return {
        "id": claim.id,
        "owner_id": claim.owner_id,
        "amount": str(claim.amount),
        "description": claim.description,
        "status": claim.status,
        "approved_by": claim.approved_by,
        "paid_by": claim.paid_by,
    }


@router.post("", status_code=201)
def submit_claim(
    request: ClaimRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    claim = Claim(owner_id=user.id, amount=request.amount, description=request.description)
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return to_dict(claim)


@router.get("")
def list_my_claims(
    status: str | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[dict]:
    query = f"SELECT id, owner_id, amount, description, status FROM claims WHERE owner_id = {user.id}"
    if status:
        # PLANTED FLAW (A05:2025 Injection): user input is pasted straight into the SQL text.
        query += f" AND status = '{status}'"
    rows = db.execute(text(query + " ORDER BY id")).mappings().all()
    return [{**row, "amount": str(row["amount"])} for row in rows]


@router.get("/{claim_id}")
def view_claim(
    claim_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    claim = db.get(Claim, claim_id)
    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")
    # PLANTED FLAW (A01:2025 Broken Access Control): checks that you are logged in, never that the claim is yours.
    return to_dict(claim)
