from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class MonitorRuleCreate(BaseModel):
    control_id: UUID | None = None
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = None
    check_type: str = "manual"
    schedule: str = "daily"
    is_active: bool = True
    config: dict | None = None


class MonitorRuleUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    check_type: str | None = None
    schedule: str | None = None
    is_active: bool | None = None
    config: dict | None = None


class MonitorRuleResponse(BaseModel):
    id: UUID
    org_id: UUID
    control_id: UUID | None
    title: str
    description: str | None
    check_type: str
    schedule: str
    is_active: bool
    config: dict | None
    last_checked_at: datetime | None
    last_result: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MonitorAlertResponse(BaseModel):
    id: UUID
    org_id: UUID
    rule_id: UUID
    severity: str
    status: str
    title: str
    details: dict | None
    triggered_at: datetime | None
    resolved_at: datetime | None
    acknowledged_by_id: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MonitorAlertUpdate(BaseModel):
    status: str | None = None  # acknowledged, resolved


class MonitoringStatsResponse(BaseModel):
    total_rules: int = 0
    active_rules: int = 0
    open_alerts: int = 0
    by_severity: dict[str, int] = {}
