import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID


class AuditFinding(BaseModel):
    __tablename__ = "audit_findings"

    audit_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("audits.id", ondelete="CASCADE"), nullable=False
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    control_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("controls.id")
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(50), default="medium")
    status: Mapped[str] = mapped_column(String(50), default="open")
    remediation_plan: Mapped[str | None] = mapped_column(Text)
    remediation_due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    remediation_owner_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )

    audit = relationship("Audit", back_populates="findings")
    control = relationship("Control")
    remediation_owner = relationship("User")
