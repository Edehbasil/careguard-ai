from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.models.audit import AuditLog
from app.schemas.audit import AuditLogResponse
from app.db.models.user import User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/audit", tags=["Audit Log"])


@router.get("/", response_model=List[AuditLogResponse])
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()


@router.get("/me", response_model=List[AuditLogResponse])
def get_my_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(AuditLog).filter(
        AuditLog.user_id == current_user.id
    ).order_by(AuditLog.timestamp.desc()).all()