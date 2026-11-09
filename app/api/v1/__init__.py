from fastapi import APIRouter

from app.api.v1.assessments import router as assessments_router
from app.api.v1.audit import router as audit_router
from app.api.v1.checklist import router as checklist_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.systems import router as systems_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(systems_router, prefix="/systems", tags=["AI systems"])
api_router.include_router(assessments_router, prefix="/assessments", tags=["Risk assessments"])
api_router.include_router(checklist_router, tags=["Checklist"])
api_router.include_router(audit_router, tags=["Audit"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
