from uuid import UUID

from fastapi import APIRouter, Query

from app.core.audit_middleware import log_audit
from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.schemas.common import PaginatedResponse, MessageResponse
from app.schemas.control import (
    BulkApproveRequest,
    ControlCreate,
    ControlResponse,
    ControlFrameworkMappingResponse,
    ControlStatsResponse,
    ControlUpdate,
)
from app.services import control_service


def _serialize_control(control) -> ControlResponse:
    """Serialize a Control ORM object with nested framework mapping details."""
    mappings = [
        ControlFrameworkMappingResponse.from_mapping(m)
        for m in (control.framework_mappings or [])
    ]
    resp = ControlResponse.model_validate(control)
    resp.framework_mappings = mappings
    return resp

router = APIRouter(prefix="/organizations/{org_id}/controls", tags=["controls"])


@router.get("", response_model=PaginatedResponse)
async def list_controls(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    status: str | None = None,
    framework_id: UUID | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    controls, total = await control_service.list_controls(
        db, org_id, status=status, framework_id=framework_id, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[_serialize_control(c) for c in controls],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=ControlResponse, status_code=201)
async def create_control(org_id: VerifiedOrgId, data: ControlCreate, db: DB, current_user: ComplianceUser):
    item = await control_service.create_control(db, org_id, data)
    await log_audit(db, current_user, "create", "control", str(item.id), org_id)
    return item


@router.get("/stats", response_model=ControlStatsResponse)
async def get_stats(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    return await control_service.get_control_stats(db, org_id)


@router.get("/{control_id}", response_model=ControlResponse)
async def get_control(org_id: VerifiedOrgId, control_id: UUID, db: DB, current_user: AnyInternalUser):
    control = await control_service.get_control(db, org_id, control_id)
    return _serialize_control(control)


@router.patch("/{control_id}", response_model=ControlResponse)
async def update_control(
    org_id: VerifiedOrgId, control_id: UUID, data: ControlUpdate, db: DB, current_user: ComplianceUser
):
    item = await control_service.update_control(db, org_id, control_id, data)
    await log_audit(db, current_user, "update", "control", str(control_id), org_id)
    return item


@router.delete("/{control_id}", status_code=204)
async def delete_control(org_id: VerifiedOrgId, control_id: UUID, db: DB, current_user: ComplianceUser):
    await control_service.delete_control(db, org_id, control_id)
    await log_audit(db, current_user, "delete", "control", str(control_id), org_id)


@router.post("/bulk-approve", response_model=MessageResponse)
async def bulk_approve(org_id: VerifiedOrgId, data: BulkApproveRequest, db: DB, current_user: ComplianceUser):
    count = await control_service.bulk_approve_controls(
        db, org_id, data.control_ids, data.status
    )
    await log_audit(db, current_user, "bulk_approve", "control", ",".join(str(i) for i in data.control_ids), org_id)
    return MessageResponse(message=f"Successfully updated {count} controls")
