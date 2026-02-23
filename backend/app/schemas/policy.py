from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class PolicyCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: str | None = None
    template_id: UUID | None = None
    status: str = "draft"
    version: str = "1.0"
    owner_id: UUID | None = None
    framework_ids: list[str] | None = None
    control_ids: list[str] | None = None


class PolicyUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    status: str | None = None
    version: str | None = None
    owner_id: UUID | None = None
    approved_by_id: UUID | None = None
    approved_at: datetime | None = None
    published_at: datetime | None = None
    next_review_date: datetime | None = None
    framework_ids: list[str] | None = None
    control_ids: list[str] | None = None


class PolicyResponse(BaseModel):
    id: UUID
    org_id: UUID
    template_id: UUID | None
    title: str
    content: str | None
    version: str
    status: str
    owner_id: UUID | None
    approved_by_id: UUID | None
    approved_at: datetime | None
    published_at: datetime | None
    next_review_date: datetime | None
    framework_ids: list | None
    control_ids: list | None
    agent_run_id: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PolicyStatsResponse(BaseModel):
    total: int
    draft: int
    in_review: int
    approved: int
    published: int
    archived: int


class PolicyTemplateResponse(BaseModel):
    id: UUID
    template_code: str
    title: str
    description: str | None
    category: str
    sections: list | None
    variables: list | None
    content_template: str | None
    required_by_frameworks: list | None
    review_frequency: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
