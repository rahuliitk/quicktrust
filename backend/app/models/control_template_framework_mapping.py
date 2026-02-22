import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import GUID


class ControlTemplateFrameworkMapping(Base):
    __tablename__ = "control_template_framework_mappings"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    control_template_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("control_templates.id"), nullable=False
    )
    framework_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("frameworks.id"), nullable=False
    )
    requirement_code: Mapped[str] = mapped_column(String(50), nullable=False)

    control_template = relationship(
        "ControlTemplate", back_populates="framework_mappings"
    )
    framework = relationship("Framework")
