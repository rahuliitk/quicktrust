from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, CurrentUser
from app.schemas.common import PaginatedResponse
from app.schemas.policy import (
    PolicyCreate,
    PolicyUpdate,
    PolicyResponse,
    PolicyStatsResponse,
)
from app.services import policy_service

router = APIRouter(prefix="/organizations/{org_id}/policies", tags=["policies"])


@router.get("", response_model=PaginatedResponse)
async def list_policies(
    org_id: UUID,
    db: DB,
    current_user: CurrentUser,
    status: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    policies, total = await policy_service.list_policies(
        db, org_id, status=status, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[PolicyResponse.model_validate(p) for p in policies],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=PolicyResponse, status_code=201)
async def create_policy(
    org_id: UUID, data: PolicyCreate, db: DB, current_user: CurrentUser
):
    return await policy_service.create_policy(db, org_id, data)


@router.get("/stats", response_model=PolicyStatsResponse)
async def get_stats(org_id: UUID, db: DB, current_user: CurrentUser):
    return await policy_service.get_policy_stats(db, org_id)


@router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(
    org_id: UUID, policy_id: UUID, db: DB, current_user: CurrentUser
):
    return await policy_service.get_policy(db, org_id, policy_id)


@router.patch("/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    org_id: UUID,
    policy_id: UUID,
    data: PolicyUpdate,
    db: DB,
    current_user: CurrentUser,
):
    return await policy_service.update_policy(db, org_id, policy_id, data)


@router.delete("/{policy_id}", status_code=204)
async def delete_policy(
    org_id: UUID, policy_id: UUID, db: DB, current_user: CurrentUser
):
    await policy_service.delete_policy(db, org_id, policy_id)
