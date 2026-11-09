from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import RiskAssessment
from app.schemas.assessment import AssessmentInput, AssessmentRead
from app.services.governance import update_assessment

router = APIRouter()


@router.get("/{assessment_id}", response_model=AssessmentRead)
def read_assessment(assessment_id: int, db: Session = Depends(get_db)):
    assessment = db.get(RiskAssessment, assessment_id)
    if assessment is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Risk assessment not found")
    return assessment


@router.put("/{assessment_id}", response_model=AssessmentRead)
def edit_assessment(assessment_id: int, payload: AssessmentInput, db: Session = Depends(get_db)):
    return update_assessment(db, assessment_id, payload)
