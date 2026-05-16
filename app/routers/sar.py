from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

from app.db.dependencies import get_db
from app.models.sar import SubjectAccessRequest, SARStatus
from app.schemas.sar import SARCreate, SARResponse, SARStatusUpdate
from app.db.models.user import User
from app.routers.auth import get_current_user
from app.utils.audit import log_action

router = APIRouter(prefix="/sar", tags=["Subject Access Requests"])


@router.post("/", response_model=SARResponse)
def submit_sar(
    sar: SARCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_sar = SubjectAccessRequest(
        requester_name=sar.requester_name,
        requester_email=sar.requester_email,
        description=sar.description,
        submitted_by_user_id=current_user.id
    )
    db.add(new_sar)
    db.commit()
    db.refresh(new_sar)

    log_action(
        db=db,
        action="CREATE",
        resource="SAR",
        user_id=current_user.id,
        resource_id=new_sar.id,
        detail=f"SAR submitted by {current_user.email}"
    )

    return _add_days_remaining(new_sar)


@router.get("/", response_model=List[SARResponse])
def list_sars(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.is_admin:
        sars = db.query(SubjectAccessRequest).all()
    else:
        sars = db.query(SubjectAccessRequest).filter(
            SubjectAccessRequest.submitted_by_user_id == current_user.id
        ).all()
    return [_add_days_remaining(s) for s in sars]


@router.get("/{sar_id}", response_model=SARResponse)
def get_sar(
    sar_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sar = db.query(SubjectAccessRequest).filter(
        SubjectAccessRequest.id == sar_id
    ).first()

    if not sar:
        raise HTTPException(status_code=404, detail="SAR not found")

    if not current_user.is_admin and sar.submitted_by_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorised to view this SAR")

    return _add_days_remaining(sar)


@router.patch("/{sar_id}/status", response_model=SARResponse)
def update_sar_status(
    sar_id: int,
    status_update: SARStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can update SAR status")

    sar = db.query(SubjectAccessRequest).filter(
        SubjectAccessRequest.id == sar_id
    ).first()

    if not sar:
        raise HTTPException(status_code=404, detail="SAR not found")

    old_status = sar.status
    sar.status = status_update.status

    if status_update.status in (SARStatus.completed, SARStatus.closed):
        sar.resolved_at = datetime.now(timezone.utc).replace(tzinfo=None)

    db.commit()
    db.refresh(sar)

    log_action(
        db=db,
        action="STATUS_UPDATE",
        resource="SAR",
        user_id=current_user.id,
        resource_id=sar.id,
        detail=f"Status changed from {old_status} to {status_update.status} by {current_user.email}"
    )

    return _add_days_remaining(sar)


def _add_days_remaining(sar: SubjectAccessRequest) -> SARResponse:
    data = SARResponse.model_validate(sar)
    if sar.deadline and sar.status not in (SARStatus.completed, SARStatus.closed):
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        delta = sar.deadline - now
        data.days_remaining = max(delta.days, 0)
    return data