from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

from app.db.dependencies import get_db
from app.models.breach import DataBreach
from app.schemas.breach import BreachCreate, BreachResponse, BreachICOUpdate, BreachResolveUpdate
from app.db.models.user import User
from app.routers.auth import get_current_user
from app.utils.audit import log_action

router = APIRouter(prefix="/breaches", tags=["Data Breach Notifications"])


@router.post("/", response_model=BreachResponse)
def report_breach(
    breach: BreachCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_breach = DataBreach(
        title=breach.title,
        description=breach.description,
        affected_individuals=breach.affected_individuals,
        data_types_affected=breach.data_types_affected,
        severity=breach.severity,
        reported_by_user_id=current_user.id
    )
    db.add(new_breach)
    db.commit()
    db.refresh(new_breach)

    log_action(
        db=db,
        action="CREATE",
        resource="DataBreach",
        user_id=current_user.id,
        resource_id=new_breach.id,
        detail=f"Data breach reported by {current_user.email} — {breach.title}"
    )

    return _add_hours_remaining(new_breach)


@router.get("/", response_model=List[BreachResponse])
def list_breaches(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    breaches = db.query(DataBreach).order_by(DataBreach.reported_at.desc()).all()
    return [_add_hours_remaining(b) for b in breaches]


@router.get("/{breach_id}", response_model=BreachResponse)
def get_breach(
    breach_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    breach = db.query(DataBreach).filter(DataBreach.id == breach_id).first()
    if not breach:
        raise HTTPException(status_code=404, detail="Breach not found")
    if not current_user.is_admin and breach.reported_by_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorised to view this breach")
    return _add_hours_remaining(breach)


@router.patch("/{breach_id}/ico", response_model=BreachResponse)
def update_ico_status(
    breach_id: int,
    update: BreachICOUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    breach = db.query(DataBreach).filter(DataBreach.id == breach_id).first()
    if not breach:
        raise HTTPException(status_code=404, detail="Breach not found")

    breach.ico_notified = update.ico_notified
    if update.ico_notified:
        breach.ico_notified_at = datetime.now(timezone.utc).replace(tzinfo=None)

    db.commit()
    db.refresh(breach)

    log_action(
        db=db,
        action="ICO_NOTIFIED",
        resource="DataBreach",
        user_id=current_user.id,
        resource_id=breach.id,
        detail=f"ICO notification status updated by {current_user.email}"
    )

    return _add_hours_remaining(breach)


@router.patch("/{breach_id}/resolve", response_model=BreachResponse)
def resolve_breach(
    breach_id: int,
    update: BreachResolveUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    breach = db.query(DataBreach).filter(DataBreach.id == breach_id).first()
    if not breach:
        raise HTTPException(status_code=404, detail="Breach not found")

    breach.resolved = update.resolved
    if update.resolved:
        breach.resolved_at = datetime.now(timezone.utc).replace(tzinfo=None)

    db.commit()
    db.refresh(breach)

    log_action(
        db=db,
        action="RESOLVED",
        resource="DataBreach",
        user_id=current_user.id,
        resource_id=breach.id,
        detail=f"Breach marked as resolved by {current_user.email}"
    )

    return _add_hours_remaining(breach)


def _add_hours_remaining(breach: DataBreach) -> BreachResponse:
    data = BreachResponse.model_validate(breach)
    if breach.ico_deadline and not breach.ico_notified:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        delta = breach.ico_deadline - now
        total_seconds = delta.total_seconds()
        data.hours_remaining = max(int(total_seconds // 3600), 0)
    return data