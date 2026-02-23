from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class OnboardingWizardInput(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=255)
    industry: str = Field(..., min_length=1, max_length=100)
    company_size: str = Field(..., min_length=1, max_length=50)
    cloud_providers: list[str] = []
    tech_stack: list[str] = []
    departments: list[str] = []
    target_framework_ids: list[UUID] = []
    compliance_timeline: str | None = None
    special_requirements: str | None = None


class OnboardingSessionResponse(BaseModel):
    id: UUID
    org_id: UUID
    status: str
    input_data: dict | None
    progress: dict | None
    results: dict | None
    agent_run_ids: dict | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
