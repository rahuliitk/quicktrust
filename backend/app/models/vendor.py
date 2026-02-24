import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class Vendor(BaseModel):
    __tablename__ = "vendors"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str | None] = mapped_column(String(100))
    website: Mapped[str | None] = mapped_column(String(500))
    risk_tier: Mapped[str] = mapped_column(String(20), default="medium")  # critical, high, medium, low
    status: Mapped[str] = mapped_column(String(50), default="active")  # active, under_review, terminated
    contact_name: Mapped[str | None] = mapped_column(String(255))
    contact_email: Mapped[str | None] = mapped_column(String(255))
    contract_start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    contract_end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_assessment_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    next_assessment_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    assessment_score: Mapped[int | None] = mapped_column(Integer)
    notes: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[dict | None] = mapped_column(JSONType(), default=list)

    organization = relationship("Organization", back_populates="vendors")
    assessments = relationship(
        "VendorAssessment", back_populates="vendor", lazy="selectin",
        cascade="all, delete-orphan"
    )


class VendorAssessment(BaseModel):
    __tablename__ = "vendor_assessments"

    vendor_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    assessed_by_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    assessment_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    score: Mapped[int | None] = mapped_column(Integer)
    risk_tier_assigned: Mapped[str | None] = mapped_column(String(20))
    notes: Mapped[str | None] = mapped_column(Text)
    questionnaire_data: Mapped[dict | None] = mapped_column(JSONType(), default=dict)

    vendor = relationship("Vendor", back_populates="assessments")
    assessed_by = relationship("User", foreign_keys=[assessed_by_id])
