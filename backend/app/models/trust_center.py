import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class TrustCenterConfig(BaseModel):
    __tablename__ = "trust_center_configs"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), unique=True, nullable=False
    )
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    headline: Mapped[str | None] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    contact_email: Mapped[str | None] = mapped_column(String(255))
    logo_url: Mapped[str | None] = mapped_column(String(500))
    certifications: Mapped[dict | None] = mapped_column(JSONType(), default=list)
    branding: Mapped[dict | None] = mapped_column(JSONType(), default=dict)

    organization = relationship("Organization", back_populates="trust_center_config")
    documents = relationship(
        "TrustCenterDocument", back_populates="config",
        foreign_keys="TrustCenterDocument.org_id",
        primaryjoin="TrustCenterConfig.org_id == TrustCenterDocument.org_id",
        lazy="selectin",
    )


class TrustCenterDocument(BaseModel):
    __tablename__ = "trust_center_documents"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    document_type: Mapped[str | None] = mapped_column(String(100))  # certification, policy, report, soc2, pentest
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    requires_nda: Mapped[bool] = mapped_column(Boolean, default=False)
    file_url: Mapped[str | None] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    valid_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    config = relationship(
        "TrustCenterConfig",
        foreign_keys=[org_id],
        primaryjoin="TrustCenterDocument.org_id == TrustCenterConfig.org_id",
        viewonly=True,
    )
