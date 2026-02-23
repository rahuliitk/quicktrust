from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class IntegrationCreate(BaseModel):
    provider: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)
    config: dict | None = None
    credentials_ref: str | None = None


class IntegrationUpdate(BaseModel):
    name: str | None = None
    status: str | None = None
    config: dict | None = None
    credentials_ref: str | None = None


class IntegrationResponse(BaseModel):
    id: UUID
    org_id: UUID
    provider: str
    name: str
    status: str
    config: dict | None
    credentials_ref: str | None
    last_sync_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CollectionTrigger(BaseModel):
    collector_type: str
    evidence_template_id: UUID | None = None
    control_id: UUID | None = None


class CollectionJobResponse(BaseModel):
    id: UUID
    org_id: UUID
    integration_id: UUID
    evidence_template_id: UUID | None
    control_id: UUID | None
    status: str
    collector_type: str
    result_data: dict | None
    evidence_id: UUID | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProviderInfo(BaseModel):
    provider: str
    name: str
    description: str
    collector_types: list[str]
