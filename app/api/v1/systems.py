from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import AISystem, AuditEvent, ChecklistItem, RiskAssessment
from app.schemas.assessment import AssessmentInput, AssessmentRead
from app.schemas.audit import AuditEventRead
from app.schemas.checklist import ChecklistCreate, ChecklistRead
from app.schemas.system import AISystemCreate, AISystemRead, AISystemUpdate
from app.services import governance

router = APIRouter()


@router.get("", response_model=list[AISystemRead])
def list_systems(db: Session = Depends(get_db)):
    return list(db.scalars(select(AISystem).order_by(AISystem.id)))


@router.post("", response_model=AISystemRead, status_code=status.HTTP_201_CREATED)
def create_system(payload: AISystemCreate, db: Session = Depends(get_db)):
    return governance.create_system(db, payload)


@router.get("/{system_id}", response_model=AISystemRead)
def read_system(system_id: int, db: Session = Depends(get_db)):
    return governance.get_system(db, system_id)


@router.put("/{system_id}", response_model=AISystemRead)
def update_system(system_id: int, payload: AISystemUpdate, db: Session = Depends(get_db)):
    return governance.update_system(db, system_id, payload)


@router.delete("/{system_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_system(system_id: int, db: Session = Depends(get_db)):
    governance.delete_system(db, system_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{system_id}/assessments", response_model=AssessmentRead, status_code=status.HTTP_201_CREATED)
def create_system_assessment(system_id: int, payload: AssessmentInput, db: Session = Depends(get_db)):
    return governance.create_assessment(db, system_id, payload)


@router.get("/{system_id}/assessments", response_model=list[AssessmentRead])
def list_system_assessments(system_id: int, db: Session = Depends(get_db)):
    governance.get_system(db, system_id)
    return list(db.scalars(select(RiskAssessment).where(RiskAssessment.ai_system_id == system_id).order_by(RiskAssessment.id.desc())))


@router.post("/{system_id}/checklist-items", response_model=ChecklistRead, status_code=status.HTTP_201_CREATED)
def create_system_checklist_item(system_id: int, payload: ChecklistCreate, db: Session = Depends(get_db)):
    return governance.create_checklist_item(db, system_id, payload)


@router.get("/{system_id}/checklist-items", response_model=list[ChecklistRead])
def list_system_checklist_items(system_id: int, db: Session = Depends(get_db)):
    governance.get_system(db, system_id)
    return list(db.scalars(select(ChecklistItem).where(ChecklistItem.ai_system_id == system_id).order_by(ChecklistItem.id)))


@router.get("/{system_id}/audit-events", response_model=list[AuditEventRead])
def list_system_audit_events(system_id: int, db: Session = Depends(get_db)):
    governance.get_system(db, system_id)
    assessment_ids = select(RiskAssessment.id).where(RiskAssessment.ai_system_id == system_id)
    checklist_ids = select(ChecklistItem.id).where(ChecklistItem.ai_system_id == system_id)
    belongs_to_system = or_(
        and_(AuditEvent.entity_type == "AI_SYSTEM", AuditEvent.entity_id == system_id),
        and_(AuditEvent.entity_type == "RISK_ASSESSMENT", AuditEvent.entity_id.in_(assessment_ids)),
        and_(AuditEvent.entity_type == "CHECKLIST_ITEM", AuditEvent.entity_id.in_(checklist_ids)),
    )
    query = select(AuditEvent).where(belongs_to_system).order_by(AuditEvent.created_at.desc(), AuditEvent.id.desc())
    return list(db.scalars(query))
