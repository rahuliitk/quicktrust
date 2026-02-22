from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    role: str = Field(default="employee", pattern=r"^(super_admin|compliance_manager|control_owner|employee|auditor)$")
    department: str | None = None


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: str | None = None
    department: str | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: UUID
    org_id: UUID
    keycloak_id: str
    email: str
    full_name: str
    role: str
    department: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
