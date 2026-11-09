from typing import Literal

from pydantic import BaseModel

from app.schemas.common import Timestamped


class AssessmentInput(BaseModel):
    personal_data_usage: bool
    automated_decision_making: bool
    customer_impact: bool
    human_oversight: bool
    transparency_available: bool
    monitoring_enabled: bool
    notes: str | None = None


class AssessmentRead(Timestamped, AssessmentInput):
    ai_system_id: int
    risk_score: int
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
