from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, AdminUser
from app.schemas.common import PaginatedResponse
from app.schemas.auditor_profile import (
    AuditorProfileCreate,
    AuditorProfileResponse,
    AuditorProfileUpdate,
)
from app.services import auditor_marketplace_service

router = APIRouter(tags=["auditor-marketplace"])


# --- Public marketplace (no org scope) ---

@router.get("/auditor-marketplace", response_model=PaginatedResponse)
async def search_marketplace(
    db: DB,
    current_user: AnyInternalUser,
    specialization: str | None = None,
    credential: str | None = None,
    location: str | None = None,
    verified_only: bool = False,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """Search the public auditor marketplace."""
    items, total = await auditor_marketplace_service.search_marketplace(
        db,
        specialization=specialization,
        credential=credential,
        location=location,
        verified_only=verified_only,
        page=page,
        page_size=page_size,
    )
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/auditor-marketplace/{profile_id}", response_model=AuditorProfileResponse)
async def get_profile(profile_id: UUID, db: DB, current_user: AnyInternalUser):
    profile = await auditor_marketplace_service.get_profile(db, profile_id)
    resp = AuditorProfileResponse.model_validate(profile)
    if profile.user:
        resp.user_name = profile.user.full_name
        resp.user_email = profile.user.email
    return resp


# --- Auditor self-management ---

@router.post("/auditor-marketplace/register", response_model=AuditorProfileResponse, status_code=201)
async def register_auditor(data: AuditorProfileCreate, db: DB, current_user: CurrentUser):
    """Register current user as an auditor in the marketplace."""
    return await auditor_marketplace_service.register_auditor(db, current_user.id, data)


@router.get("/auditor-marketplace/me/profile", response_model=AuditorProfileResponse | None)
async def get_my_profile(db: DB, current_user: CurrentUser):
    return await auditor_marketplace_service.get_my_profile(db, current_user.id)


@router.patch("/auditor-marketplace/me/profile", response_model=AuditorProfileResponse)
async def update_my_profile(data: AuditorProfileUpdate, db: DB, current_user: CurrentUser):
    return await auditor_marketplace_service.update_profile(db, current_user.id, data)


# --- Admin verification ---

@router.post("/auditor-marketplace/{profile_id}/verify", response_model=AuditorProfileResponse)
async def verify_auditor(profile_id: UUID, db: DB, current_user: AdminUser):
    """Admin: verify an auditor's credentials."""
    return await auditor_marketplace_service.verify_auditor(db, profile_id)
