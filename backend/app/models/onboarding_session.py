import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class OnboardingSession(BaseModel):
    __tablename__ = "onboarding_sessions"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(50), default="in_progress")
    input_data: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    progress: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    results: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    agent_run_ids: Mapped[dict | None] = mapped_column(JSONType(), default=dict)

    organization = relationship("Organization", back_populates="onboarding_sessions")
