from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NotificationCreate(BaseModel):
    channel: str = "in_app"
    category: str = "general"
    title: str
    message: str
    severity: str = "info"
    entity_type: str | None = None
    entity_id: str | None = None
    user_id: UUID | None = None


class NotificationResponse(BaseModel):
    id: UUID
    org_id: UUID
    user_id: UUID | None = None
    channel: str
    category: str
    title: str
    message: str
    severity: str
    entity_type: str | None = None
    entity_id: str | None = None
    is_read: bool
    read_at: datetime | None = None
    sent_at: datetime | None = None
    metadata: dict | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class NotificationStatsResponse(BaseModel):
    total: int
    unread: int
    by_category: dict[str, int]
    by_severity: dict[str, int]


class SlackWebhookCreate(BaseModel):
    webhook_url: str
    channel_name: str | None = None
    categories: list[str] | None = None


class SlackWebhookResponse(BaseModel):
    id: UUID
    org_id: UUID
    webhook_url: str
    channel_name: str | None = None
    is_active: bool
    categories: list | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationPreferenceUpdate(BaseModel):
    channel: str
    category: str
    enabled: bool
