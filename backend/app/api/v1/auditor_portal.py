"""Read-only auditor portal — authenticated via X-Auditor-Token header."""
from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.models.audit import Audit
from app.models.control import Control
from app.models.evidence import Evidence
from app.models.policy import Policy
from app.models.risk import Risk
from app.services.auditor_access_service import validate_token
from app.services.audit_service import compute_readiness_score, generate_evidence_package

router = APIRouter(prefix="/auditor/portal", tags=["auditor-portal"])


async def get_auditor_context(
    x_auditor_token: Annotated[str, Header()],
    db: AsyncSession = Depends(get_db),
) -> tuple[AsyncSession, Audit]:
    """Dependency that validates auditor token and returns db + audit."""
    _token, audit = await validate_token(db, x_auditor_token)
    return db, audit


AuditorContext = Annotated[tuple[AsyncSession, Audit], Depends(get_auditor_context)]


@router.get("/overview")
async def portal_overview(ctx: AuditorContext):
    db, audit = ctx
    readiness = await compute_readiness_score(db, audit.org_id)
    return {
        "audit": {
            "id": str(audit.id),
            "title": audit.title,
            "audit_type": audit.audit_type,
            "status": audit.status,
            "auditor_firm": audit.auditor_firm,
            "lead_auditor_name": audit.lead_auditor_name,
            "scheduled_start": audit.scheduled_start.isoformat() if audit.scheduled_start else None,
            "scheduled_end": audit.scheduled_end.isoformat() if audit.scheduled_end else None,
        },
        "readiness": {
            "overall_score": readiness["overall_score"],
            "controls_score": readiness["controls_score"],
            "evidence_score": readiness["evidence_score"],
            "policies_score": readiness["policies_score"],
            "risks_score": readiness["risks_score"],
        },
    }


@router.get("/controls")
async def portal_controls(ctx: AuditorContext):
    db, audit = ctx
    result = await db.execute(
        select(Control).where(Control.org_id == audit.org_id).order_by(Control.title)
    )
    controls = list(result.scalars().all())
    return [
        {
            "id": str(c.id),
            "title": c.title,
            "description": c.description,
            "status": c.status,
            "effectiveness": c.effectiveness,
            "automation_level": c.automation_level,
        }
        for c in controls
    ]


@router.get("/evidence")
async def portal_evidence(ctx: AuditorContext):
    db, audit = ctx
    result = await db.execute(
        select(Evidence).where(Evidence.org_id == audit.org_id).order_by(Evidence.created_at.desc())
    )
    evidence_list = list(result.scalars().all())
    return [
        {
            "id": str(e.id),
            "title": e.title,
            "status": e.status,
            "collected_at": e.collected_at.isoformat() if e.collected_at else None,
            "collection_method": e.collection_method,
            "control_id": str(e.control_id) if e.control_id else None,
            "expires_at": e.expires_at.isoformat() if e.expires_at else None,
        }
        for e in evidence_list
    ]


@router.get("/policies")
async def portal_policies(ctx: AuditorContext):
    db, audit = ctx
    result = await db.execute(
        select(Policy).where(
            Policy.org_id == audit.org_id,
            Policy.status.in_(["approved", "published"]),
        ).order_by(Policy.title)
    )
    policies = list(result.scalars().all())
    return [
        {
            "id": str(p.id),
            "title": p.title,
            "version": p.version,
            "status": p.status,
            "published_at": p.published_at.isoformat() if p.published_at else None,
        }
        for p in policies
    ]


@router.get("/risks")
async def portal_risks(ctx: AuditorContext):
    db, audit = ctx
    result = await db.execute(
        select(Risk).where(Risk.org_id == audit.org_id).order_by(Risk.risk_score.desc())
    )
    risks = list(result.scalars().all())
    return [
        {
            "id": str(r.id),
            "title": r.title,
            "category": r.category,
            "risk_level": r.risk_level,
            "risk_score": r.risk_score,
            "status": r.status,
            "treatment_type": r.treatment_type,
        }
        for r in risks
    ]


@router.get("/evidence-package")
async def portal_evidence_package(ctx: AuditorContext):
    db, audit = ctx
    return await generate_evidence_package(db, audit.org_id)
