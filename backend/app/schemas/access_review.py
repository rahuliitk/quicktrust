from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AccessReviewCampaignCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = None
    reviewer_id: UUID | None = None
    status: str = "draft"
    due_date: datetime | None = None


class AccessReviewCampaignUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    reviewer_id: UUID | None = None
    status: str | None = None
    due_date: datetime | None = None


class AccessReviewEntryCreate(BaseModel):
    user_name: str = Field(..., min_length=1)
    user_email: str = Field(..., min_length=1)
    system_name: str = Field(..., min_length=1)
    resource: str | None = None
    current_access: str | None = None


class AccessReviewEntryUpdate(BaseModel):
    decision: str | None = None  # approved, revoked, modified
    notes: str | None = None


class AccessReviewEntryResponse(BaseModel):
    id: UUID
    campaign_id: UUID
    org_id: UUID
    user_name: str
    user_email: str
    system_name: str
    resource: str | None
    current_access: str | None
    decision: str | None
    decided_by_id: UUID | None
    decided_at: datetime | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AccessReviewCampaignResponse(BaseModel):
    id: UUID
    org_id: UUID
    title: str
    description: str | None
    reviewer_id: UUID | None
    status: str
    due_date: datetime | None
    completed_at: datetime | None
    entry_count: int = 0
    pending_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AccessReviewStatsResponse(BaseModel):
    total_campaigns: int = 0
    active_campaigns: int = 0
    total_entries: int = 0
    pending_decisions: int = 0
    approved: int = 0
    revoked: int = 0
