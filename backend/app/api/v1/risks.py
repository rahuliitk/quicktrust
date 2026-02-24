from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser
from app.schemas.common import PaginatedResponse
from app.schemas.risk import (
    RiskCreate,
    RiskUpdate,
    RiskResponse,
    RiskStatsResponse,
    RiskMatrixResponse,
    RiskControlMappingCreate,
    RiskControlMappingResponse,
)
from app.services import risk_service

router = APIRouter(
    prefix="/organizations/{org_id}/risks",
    tags=["risks"],
)


@router.get("", response_model=PaginatedResponse)
async def list_risks(
    org_id: UUID,
    db: DB,
    current_user: AnyInternalUser,
    status: str | None = None,
    risk_level: str | None = None,
    category: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await risk_service.list_risks(
        db, org_id, status=status, risk_level=risk_level,
        category=category, page=page, page_size=page_size,
    )
    return PaginatedResponse(
        items=[RiskResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=RiskResponse, status_code=201)
async def create_risk(org_id: UUID, data: RiskCreate, db: DB, current_user: ComplianceUser):
    return await risk_service.create_risk(db, org_id, data)


@router.get("/stats", response_model=RiskStatsResponse)
async def get_risk_stats(org_id: UUID, db: DB, current_user: AnyInternalUser):
    return await risk_service.get_risk_stats(db, org_id)


@router.get("/matrix", response_model=RiskMatrixResponse)
async def get_risk_matrix(org_id: UUID, db: DB, current_user: AnyInternalUser):
    cells = await risk_service.get_risk_matrix(db, org_id)
    return RiskMatrixResponse(cells=cells)


@router.get("/{risk_id}", response_model=RiskResponse)
async def get_risk(org_id: UUID, risk_id: UUID, db: DB, current_user: AnyInternalUser):
    return await risk_service.get_risk(db, org_id, risk_id)


@router.patch("/{risk_id}", response_model=RiskResponse)
async def update_risk(
    org_id: UUID, risk_id: UUID, data: RiskUpdate, db: DB, current_user: ComplianceUser
):
    return await risk_service.update_risk(db, org_id, risk_id, data)


@router.delete("/{risk_id}", status_code=204)
async def delete_risk(org_id: UUID, risk_id: UUID, db: DB, current_user: ComplianceUser):
    await risk_service.delete_risk(db, org_id, risk_id)


@router.post("/{risk_id}/controls", response_model=RiskControlMappingResponse, status_code=201)
async def add_control_mapping(
    org_id: UUID, risk_id: UUID, data: RiskControlMappingCreate,
    db: DB, current_user: ComplianceUser,
):
    return await risk_service.add_control_mapping(db, org_id, risk_id, data)


@router.delete("/{risk_id}/controls/{mapping_id}", status_code=204)
async def remove_control_mapping(
    org_id: UUID, risk_id: UUID, mapping_id: UUID,
    db: DB, current_user: ComplianceUser,
):
    await risk_service.remove_control_mapping(db, org_id, risk_id, mapping_id)
