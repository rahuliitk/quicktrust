from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, AnyInternalUser, AdminUser
from app.schemas.common import PaginatedResponse, MessageResponse
from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
    NotificationStatsResponse,
    SlackWebhookCreate,
    SlackWebhookResponse,
)
from app.services import notification_service

router = APIRouter(
    prefix="/organizations/{org_id}/notifications",
    tags=["notifications"],
)


@router.get("", response_model=PaginatedResponse)
async def list_notifications(
    org_id: UUID,
    db: DB,
    current_user: AnyInternalUser,
    is_read: bool | None = None,
    category: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await notification_service.list_notifications(
        db, org_id, user_id=current_user.id, is_read=is_read,
        category=category, page=page, page_size=page_size,
    )
    return PaginatedResponse(
        items=[NotificationResponse.model_validate(n) for n in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=NotificationResponse, status_code=201)
async def create_notification(
    org_id: UUID, data: NotificationCreate, db: DB, current_user: AdminUser,
):
    return await notification_service.create_notification(db, org_id, data)


@router.get("/stats", response_model=NotificationStatsResponse)
async def get_stats(org_id: UUID, db: DB, current_user: AnyInternalUser):
    return await notification_service.get_notification_stats(
        db, org_id, user_id=current_user.id
    )


@router.post("/{notification_id}/read", response_model=NotificationResponse)
async def mark_read(
    org_id: UUID, notification_id: UUID, db: DB, current_user: AnyInternalUser,
):
    return await notification_service.mark_read(db, org_id, notification_id)


@router.post("/read-all", response_model=MessageResponse)
async def mark_all_read(org_id: UUID, db: DB, current_user: AnyInternalUser):
    count = await notification_service.mark_all_read(db, org_id, user_id=current_user.id)
    return MessageResponse(message=f"Marked {count} notifications as read")


# --- Slack webhook configuration ---

@router.post("/slack", response_model=SlackWebhookResponse, status_code=201)
async def configure_slack(
    org_id: UUID, data: SlackWebhookCreate, db: DB, current_user: AdminUser,
):
    return await notification_service.configure_slack(
        db, org_id, data.webhook_url, data.channel_name, data.categories
    )


@router.get("/slack", response_model=SlackWebhookResponse | None)
async def get_slack_config(org_id: UUID, db: DB, current_user: AdminUser):
    return await notification_service.get_slack_config(db, org_id)
