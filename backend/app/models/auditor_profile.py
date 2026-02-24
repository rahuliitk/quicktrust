import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class AuditorProfile(BaseModel):
    __tablename__ = "auditor_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), unique=True, nullable=False
    )
    firm_name: Mapped[str | None] = mapped_column(String(500))
    bio: Mapped[str | None] = mapped_column(Text)
    credentials: Mapped[list | None] = mapped_column(
        JSONType(), default=list
    )  # ["CPA", "CISA", "CISSP"]
    specializations: Mapped[list | None] = mapped_column(
        JSONType(), default=list
    )  # ["SOC 2", "ISO 27001", "HIPAA"]
    years_experience: Mapped[int | None] = mapped_column(Integer)
    location: Mapped[str | None] = mapped_column(String(255))
    hourly_rate: Mapped[float | None] = mapped_column(Float)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    rating: Mapped[float | None] = mapped_column(Float)
    total_audits: Mapped[int] = mapped_column(Integer, default=0)
    website_url: Mapped[str | None] = mapped_column(String(500))
    linkedin_url: Mapped[str | None] = mapped_column(String(500))

    user = relationship("User")
