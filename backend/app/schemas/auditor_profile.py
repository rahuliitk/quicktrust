from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AuditorProfileCreate(BaseModel):
    firm_name: str | None = None
    bio: str | None = None
    credentials: list[str] | None = None
    specializations: list[str] | None = None
    years_experience: int | None = None
    location: str | None = None
    hourly_rate: float | None = None
    is_public: bool = True
    website_url: str | None = None
    linkedin_url: str | None = None


class AuditorProfileUpdate(BaseModel):
    firm_name: str | None = None
    bio: str | None = None
    credentials: list[str] | None = None
    specializations: list[str] | None = None
    years_experience: int | None = None
    location: str | None = None
    hourly_rate: float | None = None
    is_public: bool | None = None
    website_url: str | None = None
    linkedin_url: str | None = None


class AuditorProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    firm_name: str | None = None
    bio: str | None = None
    credentials: list | None = None
    specializations: list | None = None
    years_experience: int | None = None
    location: str | None = None
    hourly_rate: float | None = None
    is_verified: bool
    verified_at: datetime | None = None
    is_public: bool
    rating: float | None = None
    total_audits: int
    website_url: str | None = None
    linkedin_url: str | None = None
    # Joined user fields
    user_name: str | None = None
    user_email: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
