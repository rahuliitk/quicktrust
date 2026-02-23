from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    report_type: str = "compliance_summary"
    format: str = "json"
    parameters: dict | None = None


class ReportResponse(BaseModel):
    id: UUID
    org_id: UUID
    title: str
    report_type: str
    format: str
    status: str
    parameters: dict | None
    generated_at: datetime | None
    file_url: str | None
    requested_by_id: UUID | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ReportStatsResponse(BaseModel):
    total: int = 0
    by_type: dict[str, int] = {}
    by_status: dict[str, int] = {}
