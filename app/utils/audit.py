from sqlalchemy.orm import Session
from app.models.audit import AuditLog


def log_action(
    db: Session,
    action: str,
    resource: str,
    user_id: int = None,
    resource_id: int = None,
    detail: str = None
):
    entry = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        resource_id=resource_id,
        detail=detail
    )
    db.add(entry)
    db.commit()