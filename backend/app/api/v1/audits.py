from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser
from app.schemas.common import PaginatedResponse
from app.schemas.audit import (
    AuditCreate, AuditUpdate, AuditResponse,
    FindingCreate, FindingUpdate, FindingResponse,
    TokenCreate, TokenResponse,
    ReadinessScoreResponse,
)
from app.services import audit_service, auditor_access_service

router = APIRouter(
    prefix="/organizations/{org_id}/audits",
    tags=["audits"],
)


@router.get("", response_model=PaginatedResponse)
async def list_audits(
    org_id: UUID, db: DB, current_user: AnyInternalUser,
    page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100),
):
    items, total = await audit_service.list_audits(db, org_id, page, page_size)
    return PaginatedResponse(
        items=[AuditResponse.model_validate(i) for i in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=AuditResponse, status_code=201)
async def create_audit(org_id: UUID, data: AuditCreate, db: DB, current_user: ComplianceUser):
    return await audit_service.create_audit(db, org_id, data)


@router.get("/readiness", response_model=ReadinessScoreResponse)
async def get_readiness_score(org_id: UUID, db: DB, current_user: AnyInternalUser):
    return await audit_service.compute_readiness_score(db, org_id)


@router.get("/{audit_id}", response_model=AuditResponse)
async def get_audit(org_id: UUID, audit_id: UUID, db: DB, current_user: AnyInternalUser):
    return await audit_service.get_audit(db, org_id, audit_id)


@router.patch("/{audit_id}", response_model=AuditResponse)
async def update_audit(
    org_id: UUID, audit_id: UUID, data: AuditUpdate,
    db: DB, current_user: ComplianceUser,
):
    return await audit_service.update_audit(db, org_id, audit_id, data)


@router.delete("/{audit_id}", status_code=204)
async def delete_audit(org_id: UUID, audit_id: UUID, db: DB, current_user: ComplianceUser):
    await audit_service.delete_audit(db, org_id, audit_id)


# --- Findings ---
@router.get("/{audit_id}/findings", response_model=list[FindingResponse])
async def list_findings(
    org_id: UUID, audit_id: UUID, db: DB, current_user: AnyInternalUser
):
    return await audit_service.list_findings(db, audit_id, org_id)


@router.post("/{audit_id}/findings", response_model=FindingResponse, status_code=201)
async def create_finding(
    org_id: UUID, audit_id: UUID, data: FindingCreate,
    db: DB, current_user: ComplianceUser,
):
    return await audit_service.create_finding(db, org_id, audit_id, data)


@router.patch("/{audit_id}/findings/{finding_id}", response_model=FindingResponse)
async def update_finding(
    org_id: UUID, audit_id: UUID, finding_id: UUID,
    data: FindingUpdate, db: DB, current_user: ComplianceUser,
):
    return await audit_service.update_finding(db, org_id, finding_id, data)


# --- Access Tokens ---
@router.get("/{audit_id}/tokens", response_model=list[TokenResponse])
async def list_tokens(
    org_id: UUID, audit_id: UUID, db: DB, current_user: ComplianceUser
):
    return await auditor_access_service.list_tokens(db, audit_id)


@router.post("/{audit_id}/tokens", response_model=TokenResponse, status_code=201)
async def create_token(
    org_id: UUID, audit_id: UUID, data: TokenCreate,
    db: DB, current_user: ComplianceUser,
):
    token_model, raw_token = await auditor_access_service.create_access_token(
        db, org_id, audit_id, data
    )
    response = TokenResponse.model_validate(token_model)
    response.token = raw_token  # Only visible once
    return response


@router.delete("/{audit_id}/tokens/{token_id}", status_code=204)
async def revoke_token(
    org_id: UUID, audit_id: UUID, token_id: UUID,
    db: DB, current_user: ComplianceUser,
):
    await auditor_access_service.revoke_token(db, org_id, audit_id, token_id)


# --- Evidence Package ---
@router.get("/{audit_id}/evidence-package")
async def get_evidence_package(
    org_id: UUID, audit_id: UUID, db: DB, current_user: AnyInternalUser
):
    await audit_service.get_audit(db, org_id, audit_id)  # verify exists
    return await audit_service.generate_evidence_package(db, org_id)
