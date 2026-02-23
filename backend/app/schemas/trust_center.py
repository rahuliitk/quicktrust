from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TrustCenterConfigCreate(BaseModel):
    slug: str = Field(..., min_length=1, max_length=255)
    is_published: bool = False
    headline: str | None = None
    description: str | None = None
    contact_email: str | None = None
    logo_url: str | None = None
    certifications: list[str] | None = None
    branding: dict | None = None


class TrustCenterConfigUpdate(BaseModel):
    is_published: bool | None = None
    slug: str | None = None
    headline: str | None = None
    description: str | None = None
    contact_email: str | None = None
    logo_url: str | None = None
    certifications: list[str] | None = None
    branding: dict | None = None


class TrustCenterConfigResponse(BaseModel):
    id: UUID
    org_id: UUID
    is_published: bool
    slug: str
    headline: str | None
    description: str | None
    contact_email: str | None
    logo_url: str | None
    certifications: list | None
    branding: dict | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TrustCenterDocumentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    document_type: str | None = None
    is_public: bool = False
    requires_nda: bool = False
    file_url: str | None = None
    description: str | None = None
    valid_until: datetime | None = None
    sort_order: int = 0


class TrustCenterDocumentUpdate(BaseModel):
    title: str | None = None
    document_type: str | None = None
    is_public: bool | None = None
    requires_nda: bool | None = None
    file_url: str | None = None
    description: str | None = None
    valid_until: datetime | None = None
    sort_order: int | None = None


class TrustCenterDocumentResponse(BaseModel):
    id: UUID
    org_id: UUID
    title: str
    document_type: str | None
    is_public: bool
    requires_nda: bool
    file_url: str | None
    description: str | None
    valid_until: datetime | None
    sort_order: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PublicTrustCenterResponse(BaseModel):
    slug: str
    headline: str | None
    description: str | None
    contact_email: str | None
    logo_url: str | None
    certifications: list | None
    branding: dict | None
    documents: list[TrustCenterDocumentResponse] = []
