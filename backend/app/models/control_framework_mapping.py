import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import GUID


class ControlFrameworkMapping(Base):
    __tablename__ = "control_framework_mappings"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    control_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("controls.id"), nullable=False
    )
    framework_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("frameworks.id"), nullable=False
    )
    requirement_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("framework_requirements.id")
    )
    objective_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("control_objectives.id")
    )

    control = relationship("Control", back_populates="framework_mappings")
    framework = relationship("Framework")
    requirement = relationship("FrameworkRequirement")
    objective = relationship("ControlObjective")
