import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import GUID


class RiskControlMapping(Base):
    __tablename__ = "risk_control_mappings"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    risk_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("risks.id", ondelete="CASCADE"), nullable=False
    )
    control_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("controls.id", ondelete="CASCADE"), nullable=False
    )
    effectiveness: Mapped[str] = mapped_column(
        String(50), default="partially_mitigates"
    )
    notes: Mapped[str | None] = mapped_column(Text)

    risk = relationship("Risk", back_populates="control_mappings")
    control = relationship("Control", back_populates="risk_mappings")
