import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class CollectionJob(BaseModel):
    __tablename__ = "collection_jobs"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    integration_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("integrations.id"), nullable=False
    )
    evidence_template_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("evidence_templates.id")
    )
    control_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("controls.id")
    )
    status: Mapped[str] = mapped_column(String(50), default="pending")
    collector_type: Mapped[str] = mapped_column(String(100), nullable=False)
    result_data: Mapped[dict | None] = mapped_column(JSONType())
    evidence_id: Mapped[uuid.UUID | None] = mapped_column(GUID())
    error_message: Mapped[str | None] = mapped_column(Text)

    integration = relationship("Integration", back_populates="collection_jobs")
