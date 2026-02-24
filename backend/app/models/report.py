import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class Report(BaseModel):
    __tablename__ = "reports"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    report_type: Mapped[str] = mapped_column(String(50), default="compliance_summary")  # compliance_summary, risk_report, evidence_audit, training_completion
    format: Mapped[str] = mapped_column(String(20), default="json")  # pdf, csv, json
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, generating, completed, failed
    parameters: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    generated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    file_url: Mapped[str | None] = mapped_column(String(500))
    requested_by_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    error_message: Mapped[str | None] = mapped_column(Text)

    organization = relationship("Organization", back_populates="reports")
    requested_by = relationship("User", foreign_keys=[requested_by_id])
