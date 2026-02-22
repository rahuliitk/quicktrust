from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ControlCreate(BaseModel):
    template_id: UUID | None = None
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = None
    implementation_details: str | None = None
    owner_id: UUID | None = None
    status: str = "draft"
    automation_level: str = "manual"
    test_procedure: str | None = None


class ControlUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    implementation_details: str | None = None
    owner_id: UUID | None = None
    status: str | None = None
    effectiveness: str | None = None
    automation_level: str | None = None
    test_procedure: str | None = None


class ControlResponse(BaseModel):
    id: UUID
    org_id: UUID
    template_id: UUID | None
    title: str
    description: str | None
    implementation_details: str | None
    owner_id: UUID | None
    status: str
    effectiveness: str | None
    automation_level: str
    test_procedure: str | None
    last_test_date: datetime | None
    last_test_result: str | None
    agent_run_id: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class BulkApproveRequest(BaseModel):
    control_ids: list[UUID]
    status: str = "implemented"


class ControlStatsResponse(BaseModel):
    total: int
    draft: int
    implemented: int
    partially_implemented: int
    not_implemented: int
    not_applicable: int
