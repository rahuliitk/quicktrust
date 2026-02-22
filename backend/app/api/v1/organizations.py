from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import DB, CurrentUser
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate,
)
from app.services import organization_service

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("", response_model=OrganizationResponse, status_code=201)
async def create_org(data: OrganizationCreate, db: DB, current_user: CurrentUser):
    return await organization_service.create_organization(db, data)


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_org(org_id: UUID, db: DB, current_user: CurrentUser):
    return await organization_service.get_organization(db, org_id)


@router.patch("/{org_id}", response_model=OrganizationResponse)
async def update_org(org_id: UUID, data: OrganizationUpdate, db: DB, current_user: CurrentUser):
    return await organization_service.update_organization(db, org_id, data)
