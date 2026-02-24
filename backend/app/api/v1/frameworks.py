from uuid import UUID

from fastapi import APIRouter, status

from app.core.dependencies import DB, AnyInternalUser, AdminUser
from app.schemas.framework import (
    DomainCreate,
    DomainDetailResponse,
    FrameworkCreate,
    FrameworkDetailResponse,
    FrameworkDomainResponse,
    FrameworkRequirementResponse,
    FrameworkResponse,
    FrameworkUpdate,
    RequirementCreate,
    RequirementDetailResponse,
)
from app.services import framework_service

router = APIRouter(prefix="/frameworks", tags=["frameworks"])


# ---------------------------------------------------------------------------
# READ endpoints (existing)
# ---------------------------------------------------------------------------


@router.get("", response_model=list[FrameworkResponse])
async def list_frameworks(db: DB, current_user: AnyInternalUser):
    return await framework_service.list_frameworks(db)


@router.get("/{framework_id}", response_model=FrameworkDetailResponse)
async def get_framework(framework_id: UUID, db: DB, current_user: AnyInternalUser):
    return await framework_service.get_framework(db, framework_id)


@router.get("/{framework_id}/domains", response_model=list[FrameworkDomainResponse])
async def get_domains(framework_id: UUID, db: DB, current_user: AnyInternalUser):
    return await framework_service.get_framework_domains(db, framework_id)


@router.get("/{framework_id}/domains/{domain_id}", response_model=DomainDetailResponse)
async def get_domain(framework_id: UUID, domain_id: UUID, db: DB, current_user: AnyInternalUser):
    return await framework_service.get_domain(db, domain_id)


@router.get("/{framework_id}/requirements", response_model=list[FrameworkRequirementResponse])
async def get_requirements(framework_id: UUID, db: DB, current_user: AnyInternalUser):
    return await framework_service.get_requirements(db, framework_id)


@router.get(
    "/{framework_id}/requirements/{requirement_id}",
    response_model=RequirementDetailResponse,
)
async def get_requirement(framework_id: UUID, requirement_id: UUID, db: DB, current_user: AnyInternalUser):
    return await framework_service.get_requirement(db, requirement_id)


# ---------------------------------------------------------------------------
# WRITE endpoints (new – Phase 4)
# ---------------------------------------------------------------------------


@router.post("", response_model=FrameworkResponse, status_code=status.HTTP_201_CREATED)
async def create_framework(data: FrameworkCreate, db: DB, current_user: AdminUser):
    """Create a new custom compliance framework."""
    return await framework_service.create_framework(db, data)


@router.patch("/{framework_id}", response_model=FrameworkResponse)
async def update_framework(framework_id: UUID, data: FrameworkUpdate, db: DB, current_user: AdminUser):
    """Update an existing framework's metadata."""
    return await framework_service.update_framework(db, framework_id, data)


@router.delete("/{framework_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_framework(framework_id: UUID, db: DB, current_user: AdminUser):
    """Delete a custom framework. Seeded frameworks cannot be deleted."""
    await framework_service.delete_framework(db, framework_id)


@router.post(
    "/{framework_id}/domains",
    response_model=FrameworkDomainResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_domain(framework_id: UUID, data: DomainCreate, db: DB, current_user: AdminUser):
    """Add a domain to an existing framework."""
    return await framework_service.add_domain(db, framework_id, data)


@router.post(
    "/{framework_id}/domains/{domain_id}/requirements",
    response_model=FrameworkRequirementResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_requirement(framework_id: UUID, domain_id: UUID, data: RequirementCreate, db: DB, current_user: AdminUser):
    """Add a requirement to a domain within a framework."""
    return await framework_service.add_requirement(db, framework_id, domain_id, data)
