import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class Audit(BaseModel):
    __tablename__ = "audits"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    framework_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("frameworks.id")
    )
    audit_type: Mapped[str] = mapped_column(String(50), default="external")
    status: Mapped[str] = mapped_column(String(50), default="planning")
    auditor_firm: Mapped[str | None] = mapped_column(String(255))
    lead_auditor_name: Mapped[str | None] = mapped_column(String(255))
    scheduled_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    scheduled_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    readiness_score: Mapped[float | None] = mapped_column(Float)

    organization = relationship("Organization", back_populates="audits")
    framework = relationship("Framework")
    findings = relationship(
        "AuditFinding", back_populates="audit", lazy="selectin",
        cascade="all, delete-orphan"
    )
    access_tokens = relationship(
        "AuditorAccessToken", back_populates="audit", lazy="selectin",
        cascade="all, delete-orphan"
    )
