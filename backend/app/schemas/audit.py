from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


# --- Audit ---
class AuditCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    framework_id: UUID | None = None
    audit_type: str = "external"
    auditor_firm: str | None = None
    lead_auditor_name: str | None = None
    scheduled_start: datetime | None = None
    scheduled_end: datetime | None = None


class AuditUpdate(BaseModel):
    title: str | None = None
    framework_id: UUID | None = None
    audit_type: str | None = None
    status: str | None = None
    auditor_firm: str | None = None
    lead_auditor_name: str | None = None
    scheduled_start: datetime | None = None
    scheduled_end: datetime | None = None


class AuditResponse(BaseModel):
    id: UUID
    org_id: UUID
    title: str
    framework_id: UUID | None
    audit_type: str
    status: str
    auditor_firm: str | None
    lead_auditor_name: str | None
    scheduled_start: datetime | None
    scheduled_end: datetime | None
    readiness_score: float | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# --- Findings ---
class FindingCreate(BaseModel):
    control_id: UUID | None = None
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = None
    severity: str = "medium"
    status: str = "open"
    remediation_plan: str | None = None
    remediation_due_date: datetime | None = None
    remediation_owner_id: UUID | None = None


class FindingUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    severity: str | None = None
    status: str | None = None
    remediation_plan: str | None = None
    remediation_due_date: datetime | None = None
    remediation_owner_id: UUID | None = None


class FindingResponse(BaseModel):
    id: UUID
    audit_id: UUID
    org_id: UUID
    control_id: UUID | None
    title: str
    description: str | None
    severity: str
    status: str
    remediation_plan: str | None
    remediation_due_date: datetime | None
    remediation_owner_id: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# --- Access Tokens ---
class TokenCreate(BaseModel):
    auditor_email: str = Field(..., min_length=1)
    auditor_name: str | None = None
    permissions: dict | None = None
    expires_at: datetime


class TokenResponse(BaseModel):
    id: UUID
    audit_id: UUID
    auditor_email: str
    auditor_name: str | None
    permissions: dict | None
    is_active: bool
    expires_at: datetime
    token: str | None = None  # Only populated on creation
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# --- Readiness ---
class ReadinessScoreResponse(BaseModel):
    overall_score: float
    controls_score: float
    evidence_score: float
    policies_score: float
    risks_score: float
    controls_implemented: int
    controls_total: int
    evidence_collected: int
    evidence_total: int
    policies_published: int
    policies_total: int
    risks_treated: int
    risks_total: int
