from uuid import UUID

from fastapi import APIRouter, Query

from app.core.audit_middleware import log_audit
from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser, VerifiedOrgId
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
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
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
    org_id: VerifiedOrgId, data: PolicyCreate, db: DB, current_user: ComplianceUser
):
    item = await policy_service.create_policy(db, org_id, data)
    await log_audit(db, current_user, "create", "policy", str(item.id), org_id)
    return item


@router.get("/stats", response_model=PolicyStatsResponse)
async def get_stats(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    return await policy_service.get_policy_stats(db, org_id)


@router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: AnyInternalUser
):
    return await policy_service.get_policy(db, org_id, policy_id)


@router.patch("/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    org_id: VerifiedOrgId,
    policy_id: UUID,
    data: PolicyUpdate,
    db: DB,
    current_user: ComplianceUser,
):
    item = await policy_service.update_policy(db, org_id, policy_id, data)
    await log_audit(db, current_user, "update", "policy", str(policy_id), org_id)
    return item


@router.delete("/{policy_id}", status_code=204)
async def delete_policy(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: ComplianceUser
):
    await policy_service.delete_policy(db, org_id, policy_id)
    await log_audit(db, current_user, "delete", "policy", str(policy_id), org_id)


# ---------------------------------------------------------------------------
# Policy workflow endpoints
# ---------------------------------------------------------------------------


@router.post("/{policy_id}/submit-for-review", response_model=PolicyResponse)
async def submit_for_review(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: ComplianceUser
):
    """Submit a draft policy for review."""
    item = await policy_service.submit_for_review(db, org_id, policy_id, current_user.id)
    await log_audit(db, current_user, "submit_for_review", "policy", str(policy_id), org_id)
    return item


@router.post("/{policy_id}/approve", response_model=PolicyResponse)
async def approve_policy(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: ComplianceUser
):
    """Approve a policy that is in review."""
    item = await policy_service.approve_policy(db, org_id, policy_id, current_user.id)
    await log_audit(db, current_user, "approve", "policy", str(policy_id), org_id)
    return item


@router.post("/{policy_id}/publish", response_model=PolicyResponse)
async def publish_policy(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: ComplianceUser
):
    """Publish an approved policy."""
    item = await policy_service.publish_policy(db, org_id, policy_id, current_user.id)
    await log_audit(db, current_user, "publish", "policy", str(policy_id), org_id)
    return item


@router.post("/{policy_id}/archive", response_model=PolicyResponse)
async def archive_policy(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: ComplianceUser
):
    """Archive a policy."""
    item = await policy_service.archive_policy(db, org_id, policy_id)
    await log_audit(db, current_user, "archive", "policy", str(policy_id), org_id)
    return item
