from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class VendorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=500)
    category: str | None = None
    website: str | None = None
    risk_tier: str = "medium"
    status: str = "active"
    contact_name: str | None = None
    contact_email: str | None = None
    contract_start_date: datetime | None = None
    contract_end_date: datetime | None = None
    notes: str | None = None
    tags: list[str] | None = None


class VendorUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    website: str | None = None
    risk_tier: str | None = None
    status: str | None = None
    contact_name: str | None = None
    contact_email: str | None = None
    contract_start_date: datetime | None = None
    contract_end_date: datetime | None = None
    next_assessment_date: datetime | None = None
    assessment_score: int | None = None
    notes: str | None = None
    tags: list[str] | None = None


class VendorAssessmentCreate(BaseModel):
    assessment_date: datetime | None = None
    score: int | None = Field(None, ge=0, le=100)
    risk_tier_assigned: str | None = None
    notes: str | None = None
    questionnaire_data: dict | None = None


class VendorAssessmentResponse(BaseModel):
    id: UUID
    vendor_id: UUID
    org_id: UUID
    assessed_by_id: UUID | None
    assessment_date: datetime | None
    score: int | None
    risk_tier_assigned: str | None
    notes: str | None
    questionnaire_data: dict | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class VendorResponse(BaseModel):
    id: UUID
    org_id: UUID
    name: str
    category: str | None
    website: str | None
    risk_tier: str
    status: str
    contact_name: str | None
    contact_email: str | None
    contract_start_date: datetime | None
    contract_end_date: datetime | None
    last_assessment_date: datetime | None
    next_assessment_date: datetime | None
    assessment_score: int | None
    notes: str | None
    tags: list | None
    assessments: list[VendorAssessmentResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class VendorStatsResponse(BaseModel):
    total: int = 0
    by_risk_tier: dict[str, int] = {}
    by_status: dict[str, int] = {}
    expiring_contracts_count: int = 0
