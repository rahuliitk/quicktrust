import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID


class FrameworkDomain(BaseModel):
    __tablename__ = "framework_domains"

    framework_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("frameworks.id"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    framework = relationship("Framework", back_populates="domains")
    requirements = relationship(
        "FrameworkRequirement", back_populates="domain", lazy="selectin"
    )
