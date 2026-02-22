from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class EvidenceCreate(BaseModel):
    control_id: UUID
    template_id: UUID | None = None
    title: str = Field(..., min_length=1, max_length=500)
    status: str = "pending"
    artifact_url: str | None = None
    data: dict | None = None
    collection_method: str = "manual"
    collector: str | None = None


class EvidenceResponse(BaseModel):
    id: UUID
    org_id: UUID
    control_id: UUID
    template_id: UUID | None
    title: str
    status: str
    collected_at: datetime | None
    expires_at: datetime | None
    artifact_url: str | None
    artifact_hash: str | None
    data: dict | None
    collection_method: str
    collector: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
