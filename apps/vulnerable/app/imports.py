"""Bulk import of claims exported from the old expense system. VULNERABLE on purpose."""

import base64
import pickle
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.db import get_db
from app.models import Claim, User

router = APIRouter(prefix="/claims", tags=["claims"])


class ImportRequest(BaseModel):
    data: str  # base64 text, as produced by the old system's export


@router.post("/import", status_code=201)
def import_claims(
    request: ImportRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    if user.role != "finance":
        raise HTTPException(status_code=403, detail="Only finance can import claims")
    # PLANTED FLAW (A08:2025 Software or Data Integrity Failures): pickle.loads runs
    # whatever instructions are inside the data, not just "read a list". Anyone who
    # can reach this endpoint can make the server execute code of their choosing.
    # Realistic origin: the old system exported Python pickles, and this was the
    # quickest way to read them.
    rows = pickle.loads(base64.b64decode(request.data))
    for row in rows:
        db.add(Claim(
            owner_id=row["owner_id"],
            amount=Decimal(str(row["amount"])),
            description=row["description"],
        ))
    db.commit()
    return {"imported": len(rows)}
