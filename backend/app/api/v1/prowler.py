"""Prowler security scanner API endpoints."""
from uuid import UUID

from fastapi import APIRouter, Query

from app.core.audit_middleware import log_audit
from app.core.dependencies import DB, ComplianceUser, AnyInternalUser, VerifiedOrgId
from app.schemas.prowler import (
    ProwlerScanTrigger,
    ProwlerScanResultResponse,
    ProwlerCompliancePosture,
    ProwlerFindingSummary,
)
from app.services import prowler_service

router = APIRouter(
    prefix="/organizations/{org_id}/prowler",
    tags=["prowler"],
)


@router.post("/scan", response_model=dict, status_code=201)
async def trigger_scan(
    org_id: VerifiedOrgId, data: ProwlerScanTrigger, db: DB, current_user: ComplianceUser
):
    """Trigger a Prowler security scan."""
    job = await prowler_service.trigger_scan(db, org_id, data)
    await log_audit(db, current_user, "trigger_prowler_scan", "prowler", str(job.id), org_id)
    return {
        "job_id": str(job.id),
        "status": job.status,
        "collector_type": job.collector_type,
    }


@router.get("/results", response_model=dict)
async def list_scan_results(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
    severity: str | None = Query(None),
    status: str | None = Query(None),
    service: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    """List Prowler scan results with optional filters."""
    items, total = await prowler_service.list_scan_results(
        db, org_id, severity=severity, status=status, service=service,
        page=page, page_size=page_size,
    )
    return {
        "items": [item.model_dump() for item in items],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


@router.get("/results/{job_id}", response_model=ProwlerScanResultResponse)
async def get_scan_detail(
    org_id: VerifiedOrgId, job_id: UUID, db: DB, current_user: AnyInternalUser
):
    """Get detailed results for a specific Prowler scan."""
    result = await prowler_service.get_scan_detail(db, org_id, job_id)
    if not result:
        from app.core.exceptions import NotFoundError
        raise NotFoundError(f"Prowler scan {job_id} not found")
    return result


@router.get("/compliance-posture", response_model=ProwlerCompliancePosture)
async def get_compliance_posture(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser
):
    """Get aggregate compliance posture from Prowler scans."""
    return await prowler_service.get_compliance_posture(db, org_id)


@router.get("/findings-summary", response_model=ProwlerFindingSummary)
async def get_findings_summary(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser
):
    """Get summary of findings from the most recent Prowler scan."""
    return await prowler_service.get_findings_summary(db, org_id)
