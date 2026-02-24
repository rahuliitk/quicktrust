from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, CurrentUser, AdminUser
from app.schemas.common import PaginatedResponse
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/organizations/{org_id}/users", tags=["users"])


@router.get("", response_model=PaginatedResponse)
async def list_users(
    org_id: UUID,
    db: DB,
    current_user: AdminUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    users, total = await user_service.list_users(db, org_id, page, page_size)
    return PaginatedResponse(
        items=[UserResponse.model_validate(u) for u in users],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(org_id: UUID, data: UserCreate, db: DB, current_user: AdminUser):
    return await user_service.create_user(db, org_id, data)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(org_id: UUID, user_id: UUID, db: DB, current_user: AdminUser):
    return await user_service.get_user(db, org_id, user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    org_id: UUID, user_id: UUID, data: UserUpdate, db: DB, current_user: AdminUser
):
    return await user_service.update_user(db, org_id, user_id, data)


@router.delete("/{user_id}", status_code=204)
async def delete_user(org_id: UUID, user_id: UUID, db: DB, current_user: AdminUser):
    await user_service.delete_user(db, org_id, user_id)
