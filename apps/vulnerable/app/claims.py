"""Claims: submit, list, view, approve and pay. VULNERABLE on purpose; flaws are marked below."""

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


@router.post("/{claim_id}/approve")
def approve_claim(
    claim_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    if user.role != "manager":
        raise HTTPException(status_code=403, detail="Only managers can approve claims")
    claim = db.get(Claim, claim_id)
    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")
    if claim.status != "submitted":
        raise HTTPException(status_code=409, detail=f"Claim is already {claim.status}")
    # PLANTED FLAW (A06:2025 Insecure Design): the design checks the approver's ROLE,
    # but has no rule that you cannot approve your OWN claim, or a claim from outside
    # your team. Separation of duties was never part of the design, so a manager can
    # approve his own expenses.
    claim.status = "approved"
    claim.approved_by = user.id
    db.commit()
    # PLANTED FLAW (A09:2025 Security Logging and Alerting Failures): money is about to
    # move and nothing records who approved what, when, or from where. The server's
    # access log shows only "POST /claims/3/approve 200", with no user.
    return to_dict(claim)


@router.post("/{claim_id}/pay")
def pay_claim(
    claim_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    if user.role != "finance":
        raise HTTPException(status_code=403, detail="Only finance can pay claims")
    claim = db.get(Claim, claim_id)
    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")
    if claim.status != "approved":
        raise HTTPException(status_code=409, detail="Only approved claims can be paid")
    claim.status = "paid"
    claim.paid_by = user.id
    db.commit()
    # Same A09 gap as approve_claim: the payment leaves no audit record.
    return to_dict(claim)
