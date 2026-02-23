import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class AuditorAccessToken(BaseModel):
    __tablename__ = "auditor_access_tokens"

    audit_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("audits.id", ondelete="CASCADE"), nullable=False
    )
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    auditor_email: Mapped[str] = mapped_column(String(255), nullable=False)
    auditor_name: Mapped[str | None] = mapped_column(String(255))
    permissions: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    audit = relationship("Audit", back_populates="access_tokens")
