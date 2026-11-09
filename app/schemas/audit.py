from datetime import datetime
from typing import Literal

from app.schemas.common import ORMModel


class AuditEventRead(ORMModel):
    id: int
    entity_type: Literal["AI_SYSTEM", "RISK_ASSESSMENT", "CHECKLIST_ITEM"]
    entity_id: int
    action: Literal["CREATE", "UPDATE", "DELETE"]
    performed_by: str
    change_summary: str
    created_at: datetime
