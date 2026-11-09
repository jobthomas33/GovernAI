from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id: Mapped[int] = mapped_column(primary_key=True)
    ai_system_id: Mapped[int] = mapped_column(ForeignKey("ai_systems.id", ondelete="CASCADE"), index=True)
    personal_data_usage: Mapped[bool] = mapped_column(Boolean, nullable=False)
    automated_decision_making: Mapped[bool] = mapped_column(Boolean, nullable=False)
    customer_impact: Mapped[bool] = mapped_column(Boolean, nullable=False)
    human_oversight: Mapped[bool] = mapped_column(Boolean, nullable=False)
    transparency_available: Mapped[bool] = mapped_column(Boolean, nullable=False)
    monitoring_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    ai_system: Mapped["AISystem"] = relationship(back_populates="assessments")
