from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.audit import Audit
from app.models.audit_finding import AuditFinding
from app.models.control import Control
from app.models.evidence import Evidence
from app.models.policy import Policy
from app.models.risk import Risk
from app.schemas.audit import (
    AuditCreate, AuditUpdate,
    FindingCreate, FindingUpdate,
)


# --- Audit CRUD ---

async def list_audits(
    db: AsyncSession, org_id: UUID, page: int = 1, page_size: int = 50
) -> tuple[list[Audit], int]:
    base_q = select(Audit).where(Audit.org_id == org_id)
    count_q = select(func.count()).select_from(Audit).where(Audit.org_id == org_id)
    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(Audit.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_audit(db: AsyncSession, org_id: UUID, data: AuditCreate) -> Audit:
    audit = Audit(org_id=org_id, **data.model_dump())
    db.add(audit)
    await db.commit()
    await db.refresh(audit)
    return audit


async def get_audit(db: AsyncSession, org_id: UUID, audit_id: UUID) -> Audit:
    result = await db.execute(
        select(Audit).where(Audit.id == audit_id, Audit.org_id == org_id)
    )
    audit = result.scalar_one_or_none()
    if not audit:
        raise NotFoundError(f"Audit {audit_id} not found")
    return audit


async def update_audit(
    db: AsyncSession, org_id: UUID, audit_id: UUID, data: AuditUpdate
) -> Audit:
    audit = await get_audit(db, org_id, audit_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(audit, key, value)
    await db.commit()
    await db.refresh(audit)
    return audit


async def delete_audit(db: AsyncSession, org_id: UUID, audit_id: UUID) -> None:
    audit = await get_audit(db, org_id, audit_id)
    await db.delete(audit)
    await db.commit()


# --- Findings ---

async def list_findings(
    db: AsyncSession, audit_id: UUID, org_id: UUID
) -> list[AuditFinding]:
    result = await db.execute(
        select(AuditFinding).where(
            AuditFinding.audit_id == audit_id,
            AuditFinding.org_id == org_id,
        ).order_by(AuditFinding.created_at.desc())
    )
    return list(result.scalars().all())


async def create_finding(
    db: AsyncSession, org_id: UUID, audit_id: UUID, data: FindingCreate
) -> AuditFinding:
    await get_audit(db, org_id, audit_id)
    finding = AuditFinding(audit_id=audit_id, org_id=org_id, **data.model_dump())
    db.add(finding)
    await db.commit()
    await db.refresh(finding)
    return finding


async def update_finding(
    db: AsyncSession, org_id: UUID, finding_id: UUID, data: FindingUpdate
) -> AuditFinding:
    result = await db.execute(
        select(AuditFinding).where(
            AuditFinding.id == finding_id, AuditFinding.org_id == org_id
        )
    )
    finding = result.scalar_one_or_none()
    if not finding:
        raise NotFoundError(f"Finding {finding_id} not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(finding, key, value)
    await db.commit()
    await db.refresh(finding)
    return finding


# --- Readiness Score ---

async def compute_readiness_score(db: AsyncSession, org_id: UUID) -> dict:
    # Controls
    controls_total = (await db.execute(
        select(func.count()).select_from(Control).where(Control.org_id == org_id)
    )).scalar() or 0
    controls_implemented = (await db.execute(
        select(func.count()).select_from(Control).where(
            Control.org_id == org_id, Control.status == "implemented"
        )
    )).scalar() or 0

    # Evidence
    evidence_total = controls_total  # one evidence per control as target
    evidence_collected = (await db.execute(
        select(func.count()).select_from(Evidence).where(
            Evidence.org_id == org_id, Evidence.status == "collected"
        )
    )).scalar() or 0

    # Policies
    policies_total = (await db.execute(
        select(func.count()).select_from(Policy).where(Policy.org_id == org_id)
    )).scalar() or 0
    policies_published = (await db.execute(
        select(func.count()).select_from(Policy).where(
            Policy.org_id == org_id, Policy.status == "published"
        )
    )).scalar() or 0

    # Risks
    risks_total = (await db.execute(
        select(func.count()).select_from(Risk).where(Risk.org_id == org_id)
    )).scalar() or 0
    risks_treated = (await db.execute(
        select(func.count()).select_from(Risk).where(
            Risk.org_id == org_id, Risk.status.in_(["accepted", "closed"])
        )
    )).scalar() or 0

    # Compute scores
    controls_pct = (controls_implemented / controls_total * 100) if controls_total else 0
    evidence_pct = (evidence_collected / evidence_total * 100) if evidence_total else 0
    policies_pct = (policies_published / policies_total * 100) if policies_total else 0
    risks_pct = (risks_treated / risks_total * 100) if risks_total else 0

    overall = (controls_pct * 0.4 + evidence_pct * 0.3 + policies_pct * 0.2 + risks_pct * 0.1)

    return {
        "overall_score": round(overall, 1),
        "controls_score": round(controls_pct, 1),
        "evidence_score": round(evidence_pct, 1),
        "policies_score": round(policies_pct, 1),
        "risks_score": round(risks_pct, 1),
        "controls_implemented": controls_implemented,
        "controls_total": controls_total,
        "evidence_collected": evidence_collected,
        "evidence_total": evidence_total,
        "policies_published": policies_published,
        "policies_total": policies_total,
        "risks_treated": risks_treated,
        "risks_total": risks_total,
    }


# --- Evidence Package ---

async def generate_evidence_package(db: AsyncSession, org_id: UUID) -> dict:
    """Generate a structured evidence package grouped by control."""
    controls_result = await db.execute(
        select(Control).where(Control.org_id == org_id).order_by(Control.title)
    )
    controls = list(controls_result.scalars().all())

    package = []
    for control in controls:
        evidence_result = await db.execute(
            select(Evidence).where(
                Evidence.org_id == org_id, Evidence.control_id == control.id
            )
        )
        evidence_list = list(evidence_result.scalars().all())
        package.append({
            "control_id": str(control.id),
            "control_title": control.title,
            "control_status": control.status,
            "evidence": [
                {
                    "id": str(e.id),
                    "title": e.title,
                    "status": e.status,
                    "collected_at": e.collected_at.isoformat() if e.collected_at else None,
                    "collection_method": e.collection_method,
                }
                for e in evidence_list
            ],
        })

    return {"controls_count": len(controls), "evidence_package": package}
