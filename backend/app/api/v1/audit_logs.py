from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, AnyInternalUser, AdminUser
from app.schemas.common import PaginatedResponse
from app.schemas.audit_log import AuditLogResponse, AuditLogStatsResponse
from app.services import audit_log_service

router = APIRouter(
    prefix="/organizations/{org_id}/audit-logs",
    tags=["audit-logs"],
)


@router.get("", response_model=PaginatedResponse)
async def list_audit_logs(
    org_id: UUID,
    db: DB,
    current_user: AdminUser,
    entity_type: str | None = None,
    entity_id: str | None = None,
    actor_id: str | None = None,
    action: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await audit_log_service.list_audit_logs(
        db, org_id,
        entity_type=entity_type, entity_id=entity_id,
        actor_id=actor_id, action=action,
        page=page, page_size=page_size,
    )
    return PaginatedResponse(
        items=[AuditLogResponse.model_validate(log) for log in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/stats", response_model=AuditLogStatsResponse)
async def get_stats(org_id: UUID, db: DB, current_user: AdminUser):
    return await audit_log_service.get_audit_log_stats(db, org_id)
