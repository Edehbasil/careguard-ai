from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.db.dependencies import get_db
from app.db.models.user import User
from app.models.sar import SubjectAccessRequest, SARStatus
from app.models.breach import DataBreach
from app.models.audit import AuditLog
from app.routers.auth import get_current_user

router = APIRouter(prefix="/summary", tags=["Admin Summary"])


@router.get("/")
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    total_sars = db.query(SubjectAccessRequest).count()
    open_sars = db.query(SubjectAccessRequest).filter(
        SubjectAccessRequest.status.in_([SARStatus.pending, SARStatus.in_progress])
    ).count()
    overdue_sars = db.query(SubjectAccessRequest).filter(
        SubjectAccessRequest.deadline < now,
        SubjectAccessRequest.status.in_([SARStatus.pending, SARStatus.in_progress])
    ).count()

    total_breaches = db.query(DataBreach).count()
    unnotified_breaches = db.query(DataBreach).filter(
        DataBreach.ico_notified == False,
        DataBreach.resolved == False
    ).count()
    overdue_breaches = db.query(DataBreach).filter(
        DataBreach.ico_deadline < now,
        DataBreach.ico_notified == False
    ).count()

    recent_audit = db.query(AuditLog).order_by(
        AuditLog.timestamp.desc()
    ).limit(5).all()

    total_users = db.query(User).count()

    return {
        "generated_at": now.isoformat(),
        "users": {
            "total": total_users
        },
        "subject_access_requests": {
            "total": total_sars,
            "open": open_sars,
            "overdue": overdue_sars
        },
        "data_breaches": {
            "total": total_breaches,
            "awaiting_ico_notification": unnotified_breaches,
            "overdue_ico_notification": overdue_breaches
        },
        "recent_activity": [
            {
                "action": log.action,
                "resource": log.resource,
                "resource_id": log.resource_id,
                "detail": log.detail,
                "timestamp": log.timestamp.isoformat()
            }
            for log in recent_audit
        ]
    }