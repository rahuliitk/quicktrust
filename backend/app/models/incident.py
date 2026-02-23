import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class Incident(BaseModel):
    __tablename__ = "incidents"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(20), default="P3")  # P1, P2, P3, P4
    status: Mapped[str] = mapped_column(String(50), default="open")  # open, investigating, resolved, closed
    category: Mapped[str | None] = mapped_column(String(100))
    assigned_to_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    detected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    post_mortem_notes: Mapped[str | None] = mapped_column(Text)
    related_control_ids: Mapped[dict | None] = mapped_column(JSONType(), default=list)

    organization = relationship("Organization", back_populates="incidents")
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])
    timeline_events = relationship(
        "IncidentTimelineEvent", back_populates="incident", lazy="selectin",
        cascade="all, delete-orphan"
    )


class IncidentTimelineEvent(BaseModel):
    __tablename__ = "incident_timeline_events"

    incident_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False
    )
    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)  # status_change, note, assignment
    description: Mapped[str] = mapped_column(Text, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    incident = relationship("Incident", back_populates="timeline_events")
    actor = relationship("User", foreign_keys=[actor_id])
