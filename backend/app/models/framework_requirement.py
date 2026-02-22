import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID


class FrameworkRequirement(BaseModel):
    __tablename__ = "framework_requirements"

    domain_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("framework_domains.id"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    domain = relationship("FrameworkDomain", back_populates="requirements")
    objectives = relationship(
        "ControlObjective", back_populates="requirement", lazy="selectin"
    )
