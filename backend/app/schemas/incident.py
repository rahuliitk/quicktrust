from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = None
    severity: str = "P3"
    status: str = "open"
    category: str | None = None
    assigned_to_id: UUID | None = None
    detected_at: datetime | None = None
    related_control_ids: list[str] | None = None


class IncidentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    severity: str | None = None
    status: str | None = None
    category: str | None = None
    assigned_to_id: UUID | None = None
    detected_at: datetime | None = None
    resolved_at: datetime | None = None
    post_mortem_notes: str | None = None
    related_control_ids: list[str] | None = None


class TimelineEventCreate(BaseModel):
    event_type: str = "note"
    description: str = Field(..., min_length=1)
    occurred_at: datetime | None = None


class TimelineEventResponse(BaseModel):
    id: UUID
    incident_id: UUID
    actor_id: UUID | None
    event_type: str
    description: str
    occurred_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class IncidentResponse(BaseModel):
    id: UUID
    org_id: UUID
    title: str
    description: str | None
    severity: str
    status: str
    category: str | None
    assigned_to_id: UUID | None
    detected_at: datetime | None
    resolved_at: datetime | None
    post_mortem_notes: str | None
    related_control_ids: list | None
    timeline_events: list[TimelineEventResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class IncidentStatsResponse(BaseModel):
    total: int = 0
    by_status: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    open_p1_count: int = 0
    avg_resolution_hours: float = 0.0
