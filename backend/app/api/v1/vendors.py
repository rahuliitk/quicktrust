from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser
from app.schemas.common import PaginatedResponse
from app.schemas.vendor import (
    VendorCreate,
    VendorUpdate,
    VendorResponse,
    VendorStatsResponse,
    VendorAssessmentCreate,
    VendorAssessmentResponse,
)
from app.services import vendor_service

router = APIRouter(
    prefix="/organizations/{org_id}/vendors",
    tags=["vendors"],
)


@router.get("", response_model=PaginatedResponse)
async def list_vendors(
    org_id: UUID,
    db: DB,
    current_user: AnyInternalUser,
    risk_tier: str | None = None,
    status: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await vendor_service.list_vendors(
        db, org_id, risk_tier=risk_tier, status=status, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[VendorResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=VendorResponse, status_code=201)
async def create_vendor(org_id: UUID, data: VendorCreate, db: DB, current_user: ComplianceUser):
    return await vendor_service.create_vendor(db, org_id, data)


@router.get("/stats", response_model=VendorStatsResponse)
async def get_vendor_stats(org_id: UUID, db: DB, current_user: AnyInternalUser):
    return await vendor_service.get_vendor_stats(db, org_id)


@router.get("/{vendor_id}", response_model=VendorResponse)
async def get_vendor(org_id: UUID, vendor_id: UUID, db: DB, current_user: AnyInternalUser):
    return await vendor_service.get_vendor(db, org_id, vendor_id)


@router.patch("/{vendor_id}", response_model=VendorResponse)
async def update_vendor(
    org_id: UUID, vendor_id: UUID, data: VendorUpdate, db: DB, current_user: ComplianceUser
):
    return await vendor_service.update_vendor(db, org_id, vendor_id, data)


@router.delete("/{vendor_id}", status_code=204)
async def delete_vendor(org_id: UUID, vendor_id: UUID, db: DB, current_user: ComplianceUser):
    await vendor_service.delete_vendor(db, org_id, vendor_id)


@router.post("/{vendor_id}/assessments", response_model=VendorAssessmentResponse, status_code=201)
async def create_assessment(
    org_id: UUID, vendor_id: UUID, data: VendorAssessmentCreate, db: DB, current_user: ComplianceUser
):
    return await vendor_service.create_assessment(db, org_id, vendor_id, data, assessed_by_id=current_user.id)


@router.get("/{vendor_id}/assessments", response_model=list[VendorAssessmentResponse])
async def get_assessments(org_id: UUID, vendor_id: UUID, db: DB, current_user: AnyInternalUser):
    return await vendor_service.get_assessments(db, org_id, vendor_id)
