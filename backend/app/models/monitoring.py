import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class MonitorRule(BaseModel):
    __tablename__ = "monitor_rules"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    control_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("controls.id")
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    check_type: Mapped[str] = mapped_column(String(50), default="manual")  # evidence_staleness, control_status, policy_expiry, manual
    schedule: Mapped[str] = mapped_column(String(20), default="daily")  # hourly, daily, weekly
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    config: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_result: Mapped[str | None] = mapped_column(String(20))  # pass, fail, error

    organization = relationship("Organization", back_populates="monitor_rules")
    control = relationship("Control", foreign_keys=[control_id])
    alerts = relationship(
        "MonitorAlert", back_populates="rule", lazy="selectin",
        cascade="all, delete-orphan"
    )


class MonitorAlert(BaseModel):
    __tablename__ = "monitor_alerts"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    rule_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("monitor_rules.id", ondelete="CASCADE"), nullable=False
    )
    severity: Mapped[str] = mapped_column(String(20), default="medium")  # critical, high, medium, low
    status: Mapped[str] = mapped_column(String(50), default="open")  # open, acknowledged, resolved
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    details: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    triggered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    acknowledged_by_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )

    rule = relationship("MonitorRule", back_populates="alerts")
    acknowledged_by = relationship("User", foreign_keys=[acknowledged_by_id])
