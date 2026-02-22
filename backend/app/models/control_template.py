from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, JSONType


class ControlTemplate(BaseModel):
    __tablename__ = "control_templates"

    template_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    domain: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    implementation_guidance: Mapped[str | None] = mapped_column(Text)
    test_procedure: Mapped[str | None] = mapped_column(Text)
    automation_level: Mapped[str] = mapped_column(String(50), default="manual")
    variables: Mapped[dict | None] = mapped_column(JSONType(), default=dict)

    framework_mappings = relationship(
        "ControlTemplateFrameworkMapping", back_populates="control_template", lazy="selectin"
    )
    evidence_templates = relationship(
        "EvidenceTemplate",
        secondary="control_template_evidence_templates",
        back_populates="control_templates",
        lazy="selectin",
    )
