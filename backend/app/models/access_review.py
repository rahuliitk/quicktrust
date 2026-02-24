import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID


class AccessReviewCampaign(BaseModel):
    __tablename__ = "access_review_campaigns"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    reviewer_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    status: Mapped[str] = mapped_column(String(50), default="draft")  # draft, active, completed, cancelled
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    organization = relationship("Organization", back_populates="access_review_campaigns")
    reviewer = relationship("User", foreign_keys=[reviewer_id])
    entries = relationship(
        "AccessReviewEntry", back_populates="campaign", lazy="selectin",
        cascade="all, delete-orphan"
    )


class AccessReviewEntry(BaseModel):
    __tablename__ = "access_review_entries"

    campaign_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("access_review_campaigns.id", ondelete="CASCADE"), nullable=False
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    user_name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_email: Mapped[str] = mapped_column(String(255), nullable=False)
    system_name: Mapped[str] = mapped_column(String(255), nullable=False)
    resource: Mapped[str | None] = mapped_column(String(500))
    current_access: Mapped[str | None] = mapped_column(String(255))
    decision: Mapped[str | None] = mapped_column(String(50))  # approved, revoked, modified, null
    decided_by_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    notes: Mapped[str | None] = mapped_column(Text)

    campaign = relationship("AccessReviewCampaign", back_populates="entries")
    decided_by = relationship("User", foreign_keys=[decided_by_id])
