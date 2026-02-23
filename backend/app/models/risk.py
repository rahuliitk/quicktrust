import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class Risk(BaseModel):
    __tablename__ = "risks"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50), default="operational")
    # Scoring
    likelihood: Mapped[int] = mapped_column(Integer, default=3)
    impact: Mapped[int] = mapped_column(Integer, default=3)
    risk_score: Mapped[int] = mapped_column(Integer, default=9)
    risk_level: Mapped[str] = mapped_column(String(20), default="medium")
    # Status workflow
    status: Mapped[str] = mapped_column(String(50), default="identified")
    # Treatment
    treatment_plan: Mapped[str | None] = mapped_column(Text)
    treatment_type: Mapped[str | None] = mapped_column(String(50))
    treatment_status: Mapped[str | None] = mapped_column(String(50))
    treatment_due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # Residual risk
    residual_likelihood: Mapped[int | None] = mapped_column(Integer)
    residual_impact: Mapped[int | None] = mapped_column(Integer)
    residual_score: Mapped[int | None] = mapped_column(Integer)
    # Ownership & review
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    reviewer_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    last_review_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    next_review_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    organization = relationship("Organization", back_populates="risks")
    owner = relationship("User", foreign_keys=[owner_id])
    reviewer = relationship("User", foreign_keys=[reviewer_id])
    control_mappings = relationship(
        "RiskControlMapping", back_populates="risk", lazy="selectin",
        cascade="all, delete-orphan"
    )
