from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser
from app.schemas.common import PaginatedResponse
from app.schemas.monitoring import (
    MonitorRuleCreate,
    MonitorRuleUpdate,
    MonitorRuleResponse,
    MonitorAlertResponse,
    MonitorAlertUpdate,
    MonitoringStatsResponse,
)
from app.services import monitoring_service

router = APIRouter(
    prefix="/organizations/{org_id}/monitoring",
    tags=["monitoring"],
)


# === Rules ===

@router.get("/rules", response_model=PaginatedResponse)
async def list_rules(
    org_id: UUID,
    db: DB,
    current_user: AnyInternalUser,
    check_type: str | None = None,
    is_active: bool | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await monitoring_service.list_rules(
        db, org_id, check_type=check_type, is_active=is_active, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[MonitorRuleResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("/rules", response_model=MonitorRuleResponse, status_code=201)
async def create_rule(org_id: UUID, data: MonitorRuleCreate, db: DB, current_user: ComplianceUser):
    return await monitoring_service.create_rule(db, org_id, data)


@router.get("/rules/{rule_id}", response_model=MonitorRuleResponse)
async def get_rule(org_id: UUID, rule_id: UUID, db: DB, current_user: AnyInternalUser):
    return await monitoring_service.get_rule(db, org_id, rule_id)


@router.patch("/rules/{rule_id}", response_model=MonitorRuleResponse)
async def update_rule(
    org_id: UUID, rule_id: UUID, data: MonitorRuleUpdate, db: DB, current_user: ComplianceUser
):
    return await monitoring_service.update_rule(db, org_id, rule_id, data)


@router.delete("/rules/{rule_id}", status_code=204)
async def delete_rule(org_id: UUID, rule_id: UUID, db: DB, current_user: ComplianceUser):
    await monitoring_service.delete_rule(db, org_id, rule_id)


@router.post("/rules/{rule_id}/run", response_model=list[MonitorAlertResponse])
async def run_rule(org_id: UUID, rule_id: UUID, db: DB, current_user: ComplianceUser):
    return await monitoring_service.run_checks(db, org_id, rule_id)


@router.get("/stats", response_model=MonitoringStatsResponse)
async def get_stats(org_id: UUID, db: DB, current_user: AnyInternalUser):
    return await monitoring_service.get_monitoring_stats(db, org_id)


# === Alerts ===

@router.get("/alerts", response_model=PaginatedResponse)
async def list_alerts(
    org_id: UUID,
    db: DB,
    current_user: AnyInternalUser,
    status: str | None = None,
    severity: str | None = None,
    rule_id: UUID | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await monitoring_service.list_alerts(
        db, org_id, status=status, severity=severity, rule_id=rule_id,
        page=page, page_size=page_size,
    )
    return PaginatedResponse(
        items=[MonitorAlertResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.patch("/alerts/{alert_id}", response_model=MonitorAlertResponse)
async def update_alert(
    org_id: UUID, alert_id: UUID, data: MonitorAlertUpdate, db: DB, current_user: ComplianceUser
):
    return await monitoring_service.update_alert(db, org_id, alert_id, data, user_id=current_user.id)
