from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, JSONType


class EvidenceTemplate(BaseModel):
    __tablename__ = "evidence_templates"

    template_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    evidence_type: Mapped[str] = mapped_column(String(50), nullable=False)
    format: Mapped[str | None] = mapped_column(String(50))
    collection_method: Mapped[str] = mapped_column(String(50), default="manual")
    refresh_frequency: Mapped[str | None] = mapped_column(String(50))
    retention_period: Mapped[str | None] = mapped_column(String(50))
    fields: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    pass_criteria: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    integrations: Mapped[dict | None] = mapped_column(JSONType(), default=dict)

    control_templates = relationship(
        "ControlTemplate",
        secondary="control_template_evidence_templates",
        back_populates="evidence_templates",
        lazy="selectin",
    )
