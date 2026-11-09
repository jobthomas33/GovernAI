from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import AISystem, AuditEvent, ChecklistItem, RiskAssessment
from app.repositories.common import add_audit
from app.schemas.assessment import AssessmentInput
from app.schemas.checklist import ChecklistCreate, ChecklistUpdate
from app.schemas.system import AISystemCreate, AISystemUpdate
from app.utils.checklist import calculate_completion_percent
from app.utils.risk_scoring import calculate_risk_score


def get_system(db: Session, system_id: int) -> AISystem:
    system = db.get(AISystem, system_id)
    if system is None:
        raise HTTPException(status_code=404, detail="AI system not found")
    return system


def create_system(db: Session, data: AISystemCreate) -> AISystem:
    system = AISystem(**data.model_dump())
    db.add(system)
    db.flush()
    add_audit(db, "AI_SYSTEM", system.id, "CREATE", f"Created AI system '{system.name}'")
    db.commit()
    db.refresh(system)
    return system


def update_system(db: Session, system_id: int, data: AISystemUpdate) -> AISystem:
    system = get_system(db, system_id)
    changes = data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(system, key, value)
    add_audit(db, "AI_SYSTEM", system.id, "UPDATE", f"Updated AI system fields: {', '.join(changes) or 'no fields'}")
    db.commit()
    db.refresh(system)
    return system


def delete_system(db: Session, system_id: int) -> None:
    system = get_system(db, system_id)
    add_audit(db, "AI_SYSTEM", system.id, "DELETE", f"Deleted AI system '{system.name}'")
    db.delete(system)
    db.commit()


def create_assessment(db: Session, system_id: int, data: AssessmentInput) -> RiskAssessment:
    get_system(db, system_id)
    fields = data.model_dump()
    score, level = calculate_risk_score(**{key: fields[key] for key in (
        "personal_data_usage", "automated_decision_making", "customer_impact",
        "human_oversight", "transparency_available", "monitoring_enabled",
    )})
    assessment = RiskAssessment(ai_system_id=system_id, **fields, risk_score=score, risk_level=level)
    db.add(assessment)
    db.flush()
    add_audit(db, "RISK_ASSESSMENT", assessment.id, "CREATE", f"Created {level} risk assessment (score {score})")
    db.commit()
    db.refresh(assessment)
    return assessment


def update_assessment(db: Session, assessment_id: int, data: AssessmentInput) -> RiskAssessment:
    assessment = db.get(RiskAssessment, assessment_id)
    if assessment is None:
        raise HTTPException(status_code=404, detail="Risk assessment not found")
    fields = data.model_dump()
    score, level = calculate_risk_score(**{key: fields[key] for key in (
        "personal_data_usage", "automated_decision_making", "customer_impact",
        "human_oversight", "transparency_available", "monitoring_enabled",
    )})
    for key, value in fields.items():
        setattr(assessment, key, value)
    assessment.risk_score, assessment.risk_level = score, level
    add_audit(db, "RISK_ASSESSMENT", assessment.id, "UPDATE", f"Updated assessment; risk is {level} (score {score})")
    db.commit()
    db.refresh(assessment)
    return assessment


def create_checklist_item(db: Session, system_id: int, data: ChecklistCreate) -> ChecklistItem:
    get_system(db, system_id)
    values = data.model_dump()
    item = ChecklistItem(ai_system_id=system_id, **values,
                         completed_at=datetime.now(timezone.utc) if values["is_completed"] else None)
    db.add(item)
    db.flush()
    add_audit(db, "CHECKLIST_ITEM", item.id, "CREATE", f"Created checklist item '{item.item_name}'")
    db.commit()
    db.refresh(item)
    return item


def update_checklist_item(db: Session, item_id: int, data: ChecklistUpdate) -> ChecklistItem:
    item = db.get(ChecklistItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Checklist item not found")
    changes = data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(item, key, value)
    if "is_completed" in changes:
        item.completed_at = datetime.now(timezone.utc) if item.is_completed else None
    add_audit(db, "CHECKLIST_ITEM", item.id, "UPDATE", f"Updated checklist item '{item.item_name}'")
    db.commit()
    db.refresh(item)
    return item


def delete_checklist_item(db: Session, item_id: int) -> None:
    item = db.get(ChecklistItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Checklist item not found")
    add_audit(db, "CHECKLIST_ITEM", item.id, "DELETE", f"Deleted checklist item '{item.item_name}'")
    db.delete(item)
    db.commit()


def dashboard_summary(db: Session) -> dict:
    total = db.scalar(select(func.count(AISystem.id))) or 0
    latest_levels = select(RiskAssessment.ai_system_id, func.max(RiskAssessment.id).label("assessment_id")).group_by(RiskAssessment.ai_system_id).subquery()
    level_counts = {level: db.scalar(select(func.count()).select_from(RiskAssessment).join(latest_levels, RiskAssessment.id == latest_levels.c.assessment_id).where(RiskAssessment.risk_level == level)) or 0 for level in ("LOW", "MEDIUM", "HIGH")}
    item_count = db.scalar(select(func.count(ChecklistItem.id))) or 0
    completed = db.scalar(select(func.count(ChecklistItem.id)).where(ChecklistItem.is_completed.is_(True))) or 0
    events = list(db.scalars(select(AuditEvent).order_by(AuditEvent.created_at.desc(), AuditEvent.id.desc()).limit(10)))
    return {"total_systems": total, "high_risk_systems": level_counts["HIGH"],
            "medium_risk_systems": level_counts["MEDIUM"], "low_risk_systems": level_counts["LOW"],
            "checklist_completion_percent": calculate_completion_percent(completed, item_count),
            "recent_audit_events": events}
