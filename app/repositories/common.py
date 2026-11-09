from sqlalchemy.orm import Session

from app.models.audit_event import AuditEvent


def add_audit(db: Session, entity_type: str, entity_id: int, action: str, summary: str) -> None:
    db.add(AuditEvent(entity_type=entity_type, entity_id=entity_id, action=action, change_summary=summary))
