from uuid import UUID

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.core.dependencies import DB, AdminUser
from app.schemas.common import PaginatedResponse
from app.services import tenant_service

router = APIRouter(prefix="/tenants", tags=["tenants"])


class TenantProvisionRequest(BaseModel):
    name: str
    industry: str | None = None
    company_size: str | None = None
    admin_email: str | None = None
    admin_name: str | None = None
    admin_keycloak_id: str | None = None


@router.post("/provision", status_code=201)
async def provision_tenant(data: TenantProvisionRequest, db: DB, current_user: AdminUser):
    """Provision a new tenant organization (super admin only)."""
    return await tenant_service.provision_tenant(
        db,
        name=data.name,
        industry=data.industry,
        company_size=data.company_size,
        admin_email=data.admin_email,
        admin_name=data.admin_name,
        admin_keycloak_id=data.admin_keycloak_id,
    )


@router.get("", response_model=PaginatedResponse)
async def list_tenants(
    db: DB,
    current_user: AdminUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    """List all tenants (super admin only)."""
    items, total = await tenant_service.list_tenants(db, page=page, page_size=page_size)
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/{org_id}/isolation-check")
async def check_tenant_isolation(org_id: UUID, db: DB, current_user: AdminUser):
    """Run tenant isolation verification checks (super admin only)."""
    return await tenant_service.verify_tenant_isolation(db, org_id)
