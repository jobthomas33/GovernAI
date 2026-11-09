from app.schemas.audit import AuditEventRead
from app.schemas.common import ORMModel


class DashboardSummary(ORMModel):
    total_systems: int
    high_risk_systems: int
    medium_risk_systems: int
    low_risk_systems: int
    checklist_completion_percent: float
    recent_audit_events: list[AuditEventRead]
