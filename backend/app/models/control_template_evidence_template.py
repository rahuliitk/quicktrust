import uuid

from sqlalchemy import Column, ForeignKey, Table

from app.core.database import Base
from app.models.base import GUID

control_template_evidence_templates = Table(
    "control_template_evidence_templates",
    Base.metadata,
    Column("id", GUID(), primary_key=True, default=uuid.uuid4),
    Column(
        "control_template_id",
        GUID(),
        ForeignKey("control_templates.id"),
        nullable=False,
    ),
    Column(
        "evidence_template_id",
        GUID(),
        ForeignKey("evidence_templates.id"),
        nullable=False,
    ),
)
