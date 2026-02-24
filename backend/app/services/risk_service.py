from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import cache_get, cache_set, cache_delete
from app.core.exceptions import NotFoundError
from app.models.risk import Risk
from app.models.risk_control_mapping import RiskControlMapping
from app.schemas.risk import RiskCreate, RiskUpdate, RiskControlMappingCreate


def compute_risk_score(likelihood: int, impact: int) -> int:
    return likelihood * impact


def compute_risk_level(score: int) -> str:
    if score >= 20:
        return "critical"
    elif score >= 12:
        return "high"
    elif score >= 5:
        return "medium"
    return "low"


async def list_risks(
    db: AsyncSession,
    org_id: UUID,
    status: str | None = None,
    risk_level: str | None = None,
    category: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[Risk], int]:
    base_q = select(Risk).where(Risk.org_id == org_id)
    count_q = select(func.count()).select_from(Risk).where(Risk.org_id == org_id)

    if status:
        base_q = base_q.where(Risk.status == status)
        count_q = count_q.where(Risk.status == status)
    if risk_level:
        base_q = base_q.where(Risk.risk_level == risk_level)
        count_q = count_q.where(Risk.risk_level == risk_level)
    if category:
        base_q = base_q.where(Risk.category == category)
        count_q = count_q.where(Risk.category == category)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(Risk.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_risk(db: AsyncSession, org_id: UUID, data: RiskCreate) -> Risk:
    fields = data.model_dump()
    score = compute_risk_score(fields["likelihood"], fields["impact"])
    level = compute_risk_level(score)
    residual_score = None
    if fields.get("residual_likelihood") and fields.get("residual_impact"):
        residual_score = compute_risk_score(fields["residual_likelihood"], fields["residual_impact"])

    risk = Risk(
        org_id=org_id,
        risk_score=score,
        risk_level=level,
        residual_score=residual_score,
        **fields,
    )
    db.add(risk)
    await db.commit()
    await db.refresh(risk)
    await cache_delete(f"org:{org_id}:risk_stats")
    return risk


async def get_risk(db: AsyncSession, org_id: UUID, risk_id: UUID) -> Risk:
    result = await db.execute(
        select(Risk).where(Risk.id == risk_id, Risk.org_id == org_id)
    )
    risk = result.scalar_one_or_none()
    if not risk:
        raise NotFoundError(f"Risk {risk_id} not found")
    return risk


async def update_risk(db: AsyncSession, org_id: UUID, risk_id: UUID, data: RiskUpdate) -> Risk:
    risk = await get_risk(db, org_id, risk_id)
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(risk, key, value)

    # Recompute scores
    risk.risk_score = compute_risk_score(risk.likelihood, risk.impact)
    risk.risk_level = compute_risk_level(risk.risk_score)
    if risk.residual_likelihood and risk.residual_impact:
        risk.residual_score = compute_risk_score(risk.residual_likelihood, risk.residual_impact)

    await db.commit()
    await db.refresh(risk)
    await cache_delete(f"org:{org_id}:risk_stats")
    return risk


async def delete_risk(db: AsyncSession, org_id: UUID, risk_id: UUID) -> None:
    risk = await get_risk(db, org_id, risk_id)
    await db.delete(risk)
    await db.commit()
    await cache_delete(f"org:{org_id}:risk_stats")


async def get_risk_stats(db: AsyncSession, org_id: UUID) -> dict:
    cache_key = f"org:{org_id}:risk_stats"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    risks_result = await db.execute(select(Risk).where(Risk.org_id == org_id))
    risks = list(risks_result.scalars().all())

    by_status: dict[str, int] = {}
    by_level: dict[str, int] = {}
    total_score = 0

    for r in risks:
        by_status[r.status] = by_status.get(r.status, 0) + 1
        by_level[r.risk_level] = by_level.get(r.risk_level, 0) + 1
        total_score += r.risk_score

    stats = {
        "total": len(risks),
        "by_status": by_status,
        "by_risk_level": by_level,
        "average_score": round(total_score / len(risks), 1) if risks else 0.0,
    }
    await cache_set(cache_key, stats, ttl=120)
    return stats


async def get_risk_matrix(db: AsyncSession, org_id: UUID) -> list[dict]:
    risks_result = await db.execute(select(Risk).where(Risk.org_id == org_id))
    risks = list(risks_result.scalars().all())

    grid: dict[tuple[int, int], list[str]] = {}
    for r in risks:
        key = (r.likelihood, r.impact)
        grid.setdefault(key, []).append(str(r.id))

    cells = []
    for (likelihood, impact), risk_ids in grid.items():
        cells.append({
            "likelihood": likelihood,
            "impact": impact,
            "count": len(risk_ids),
            "risk_ids": risk_ids,
        })
    return cells


async def add_control_mapping(
    db: AsyncSession, org_id: UUID, risk_id: UUID, data: RiskControlMappingCreate
) -> RiskControlMapping:
    await get_risk(db, org_id, risk_id)  # verify exists
    mapping = RiskControlMapping(
        risk_id=risk_id,
        control_id=data.control_id,
        effectiveness=data.effectiveness,
        notes=data.notes,
    )
    db.add(mapping)
    await db.commit()
    await db.refresh(mapping)
    return mapping


async def remove_control_mapping(
    db: AsyncSession, org_id: UUID, risk_id: UUID, mapping_id: UUID
) -> None:
    await get_risk(db, org_id, risk_id)  # verify exists
    result = await db.execute(
        select(RiskControlMapping).where(
            RiskControlMapping.id == mapping_id,
            RiskControlMapping.risk_id == risk_id,
        )
    )
    mapping = result.scalar_one_or_none()
    if not mapping:
        raise NotFoundError(f"Mapping {mapping_id} not found")
    await db.delete(mapping)
    await db.commit()
