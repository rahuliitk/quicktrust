from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: UUID
    org_id: UUID
    actor_type: str
    actor_id: str
    action: str
    entity_type: str
    entity_id: str
    changes: dict | None = None
    ip_address: str | None = None
    timestamp: datetime

    model_config = {"from_attributes": True}


class AuditLogStatsResponse(BaseModel):
    total: int
    by_action: dict[str, int]
    by_entity_type: dict[str, int]
