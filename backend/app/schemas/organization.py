from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$")
    industry: str | None = None
    company_size: str | None = None
    cloud_providers: dict | None = None
    tech_stack: dict | None = None
    settings: dict | None = None


class OrganizationUpdate(BaseModel):
    name: str | None = None
    industry: str | None = None
    company_size: str | None = None
    cloud_providers: dict | None = None
    tech_stack: dict | None = None
    settings: dict | None = None


class OrganizationResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    industry: str | None
    company_size: str | None
    cloud_providers: dict | None
    tech_stack: dict | None
    settings: dict | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
