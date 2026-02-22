from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EvidenceTemplateResponse(BaseModel):
    id: UUID
    template_code: str
    title: str
    description: str | None
    evidence_type: str
    format: str | None
    collection_method: str
    refresh_frequency: str | None
    retention_period: str | None
    fields: dict | None
    pass_criteria: dict | None
    integrations: dict | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EvidenceTemplateBriefResponse(BaseModel):
    id: UUID
    template_code: str
    title: str
    evidence_type: str
    collection_method: str

    model_config = {"from_attributes": True}
