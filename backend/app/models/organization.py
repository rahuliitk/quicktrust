from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, JSONType


class Organization(BaseModel):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    industry: Mapped[str | None] = mapped_column(String(255))
    company_size: Mapped[str | None] = mapped_column(String(50))
    cloud_providers: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    tech_stack: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    settings: Mapped[dict | None] = mapped_column(JSONType(), default=dict)

    users = relationship("User", back_populates="organization", lazy="selectin")
    controls = relationship("Control", back_populates="organization", lazy="selectin")
    evidence = relationship("Evidence", back_populates="organization", lazy="selectin")
    agent_runs = relationship("AgentRun", back_populates="organization", lazy="selectin")
    policies = relationship("Policy", back_populates="organization", lazy="selectin")
    risks = relationship("Risk", back_populates="organization", lazy="selectin")
    integrations = relationship("Integration", back_populates="organization", lazy="selectin")
    audits = relationship("Audit", back_populates="organization", lazy="selectin")
    onboarding_sessions = relationship("OnboardingSession", back_populates="organization", lazy="selectin")
    incidents = relationship("Incident", back_populates="organization", lazy="selectin")
    vendors = relationship("Vendor", back_populates="organization", lazy="selectin")
    training_courses = relationship("TrainingCourse", back_populates="organization", lazy="selectin")
    access_review_campaigns = relationship("AccessReviewCampaign", back_populates="organization", lazy="selectin")
    monitor_rules = relationship("MonitorRule", back_populates="organization", lazy="selectin")
    questionnaires = relationship("Questionnaire", back_populates="organization", lazy="selectin")
    trust_center_config = relationship("TrustCenterConfig", back_populates="organization", uselist=False, lazy="selectin")
    reports = relationship("Report", back_populates="organization", lazy="selectin")
