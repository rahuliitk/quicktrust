import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class Notification(BaseModel):
    __tablename__ = "notifications"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    channel: Mapped[str] = mapped_column(
        String(50), nullable=False, default="in_app"
    )  # in_app, email, slack
    category: Mapped[str] = mapped_column(
        String(100), nullable=False, default="general"
    )  # policy_expiry, evidence_stale, incident, monitoring_alert, access_review, training
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(
        String(20), default="info"
    )  # info, warning, critical
    entity_type: Mapped[str | None] = mapped_column(String(100))
    entity_id: Mapped[str | None] = mapped_column(String(255))
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    extra_data: Mapped[dict | None] = mapped_column(JSONType(), default=dict)

    organization = relationship("Organization")
    user = relationship("User")


class NotificationPreference(BaseModel):
    __tablename__ = "notification_preferences"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False
    )
    channel: Mapped[str] = mapped_column(String(50), nullable=False)  # email, slack, in_app
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class SlackWebhookConfig(BaseModel):
    __tablename__ = "slack_webhook_configs"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    webhook_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    channel_name: Mapped[str | None] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    categories: Mapped[list | None] = mapped_column(JSONType(), default=list)
