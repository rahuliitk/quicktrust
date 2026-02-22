from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.evidence import Evidence
from app.schemas.evidence import EvidenceCreate


async def list_evidence(
    db: AsyncSession,
    org_id: UUID,
    control_id: UUID | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[Evidence], int]:
    base_q = select(Evidence).where(Evidence.org_id == org_id)
    count_base = select(func.count()).select_from(Evidence).where(Evidence.org_id == org_id)

    if control_id:
        base_q = base_q.where(Evidence.control_id == control_id)
        count_base = count_base.where(Evidence.control_id == control_id)

    total = (await db.execute(count_base)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(Evidence.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_evidence(db: AsyncSession, org_id: UUID, data: EvidenceCreate) -> Evidence:
    evidence = Evidence(
        org_id=org_id,
        collected_at=datetime.now(timezone.utc),
        **data.model_dump(),
    )
    db.add(evidence)
    await db.commit()
    await db.refresh(evidence)
    return evidence


async def get_evidence(db: AsyncSession, org_id: UUID, evidence_id: UUID) -> Evidence:
    result = await db.execute(
        select(Evidence).where(Evidence.id == evidence_id, Evidence.org_id == org_id)
    )
    evidence = result.scalar_one_or_none()
    if not evidence:
        raise NotFoundError(f"Evidence {evidence_id} not found")
    return evidence
