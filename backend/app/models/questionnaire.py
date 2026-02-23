import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class Questionnaire(BaseModel):
    __tablename__ = "questionnaires"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    source: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="draft")  # draft, in_progress, completed, submitted
    questions: Mapped[dict | None] = mapped_column(JSONType(), default=list)
    total_questions: Mapped[int] = mapped_column(Integer, default=0)
    answered_count: Mapped[int] = mapped_column(Integer, default=0)

    organization = relationship("Organization", back_populates="questionnaires")
    responses = relationship(
        "QuestionnaireResponse", back_populates="questionnaire", lazy="selectin",
        cascade="all, delete-orphan"
    )


class QuestionnaireResponse(BaseModel):
    __tablename__ = "questionnaire_responses"

    questionnaire_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("questionnaires.id", ondelete="CASCADE"), nullable=False
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    question_id: Mapped[str] = mapped_column(String(100), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[float | None] = mapped_column(Float)
    source_type: Mapped[str | None] = mapped_column(String(50))  # control, policy, manual
    source_id: Mapped[uuid.UUID | None] = mapped_column(GUID())
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    approved_by_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )

    questionnaire = relationship("Questionnaire", back_populates="responses")
    approved_by = relationship("User", foreign_keys=[approved_by_id])
