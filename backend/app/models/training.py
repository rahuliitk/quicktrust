import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class TrainingCourse(BaseModel):
    __tablename__ = "training_courses"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    content_url: Mapped[str | None] = mapped_column(String(500))
    course_type: Mapped[str] = mapped_column(String(50), default="document")  # video, document, quiz
    required_roles: Mapped[dict | None] = mapped_column(JSONType(), default=list)
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
    is_required: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    organization = relationship("Organization", back_populates="training_courses")
    assignments = relationship(
        "TrainingAssignment", back_populates="course", lazy="selectin",
        cascade="all, delete-orphan"
    )


class TrainingAssignment(BaseModel):
    __tablename__ = "training_assignments"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("training_courses.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(50), default="assigned")  # assigned, in_progress, completed, overdue
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    score: Mapped[int | None] = mapped_column(Integer)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    assigned_by_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )

    course = relationship("TrainingCourse", back_populates="assignments")
    user = relationship("User", foreign_keys=[user_id])
    assigned_by = relationship("User", foreign_keys=[assigned_by_id])
