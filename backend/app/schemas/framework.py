from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class FrameworkResponse(BaseModel):
    id: UUID
    name: str
    version: str
    category: str | None
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class FrameworkDomainResponse(BaseModel):
    id: UUID
    framework_id: UUID
    code: str
    name: str
    description: str | None
    sort_order: int
    created_at: datetime

    model_config = {"from_attributes": True}


class FrameworkRequirementResponse(BaseModel):
    id: UUID
    domain_id: UUID
    code: str
    title: str
    description: str | None
    sort_order: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ControlObjectiveResponse(BaseModel):
    id: UUID
    requirement_id: UUID
    code: str
    title: str
    description: str | None
    sort_order: int
    created_at: datetime

    model_config = {"from_attributes": True}


class FrameworkDetailResponse(FrameworkResponse):
    domains: list[FrameworkDomainResponse] = []


class DomainDetailResponse(FrameworkDomainResponse):
    requirements: list[FrameworkRequirementResponse] = []


class RequirementDetailResponse(FrameworkRequirementResponse):
    objectives: list[ControlObjectiveResponse] = []
