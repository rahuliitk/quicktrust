from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AgentRunTrigger(BaseModel):
    framework_id: UUID
    company_context: dict | None = None


class AgentRunTriggerGeneric(BaseModel):
    """Generic trigger for agents that accept flexible input."""
    framework_id: UUID | None = None
    audit_id: UUID | None = None
    vendor_id: UUID | None = None
    company_context: dict | None = None


class AgentRunResponse(BaseModel):
    id: UUID
    org_id: UUID
    agent_type: str
    trigger: str
    status: str
    input_data: dict | None
    output_data: dict | None
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None
    tokens_used: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
