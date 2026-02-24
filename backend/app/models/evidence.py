import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class Evidence(BaseModel):
    __tablename__ = "evidence"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    control_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("controls.id"), nullable=False
    )
    template_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("evidence_templates.id")
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    collected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    artifact_url: Mapped[str | None] = mapped_column(String(1000))
    artifact_hash: Mapped[str | None] = mapped_column(String(255))
    file_url: Mapped[str | None] = mapped_column(String(1000))
    file_name: Mapped[str | None] = mapped_column(String(500))
    data: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    collection_method: Mapped[str] = mapped_column(String(50), default="manual")
    collector: Mapped[str | None] = mapped_column(String(255))

    organization = relationship("Organization", back_populates="evidence")
    control = relationship("Control", back_populates="evidence")
    template = relationship("EvidenceTemplate")
