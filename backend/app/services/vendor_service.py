from datetime import datetime, timezone, timedelta
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.vendor import Vendor, VendorAssessment
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorAssessmentCreate


async def list_vendors(
    db: AsyncSession,
    org_id: UUID,
    risk_tier: str | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[Vendor], int]:
    base_q = select(Vendor).where(Vendor.org_id == org_id)
    count_q = select(func.count()).select_from(Vendor).where(Vendor.org_id == org_id)

    if risk_tier:
        base_q = base_q.where(Vendor.risk_tier == risk_tier)
        count_q = count_q.where(Vendor.risk_tier == risk_tier)
    if status:
        base_q = base_q.where(Vendor.status == status)
        count_q = count_q.where(Vendor.status == status)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(Vendor.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_vendor(db: AsyncSession, org_id: UUID, data: VendorCreate) -> Vendor:
    vendor = Vendor(org_id=org_id, **data.model_dump())
    db.add(vendor)
    await db.commit()
    await db.refresh(vendor)
    return vendor


async def get_vendor(db: AsyncSession, org_id: UUID, vendor_id: UUID) -> Vendor:
    result = await db.execute(
        select(Vendor).where(Vendor.id == vendor_id, Vendor.org_id == org_id)
    )
    vendor = result.scalar_one_or_none()
    if not vendor:
        raise NotFoundError(f"Vendor {vendor_id} not found")
    return vendor


async def update_vendor(
    db: AsyncSession, org_id: UUID, vendor_id: UUID, data: VendorUpdate
) -> Vendor:
    vendor = await get_vendor(db, org_id, vendor_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(vendor, field, value)
    await db.commit()
    await db.refresh(vendor)
    return vendor


async def delete_vendor(db: AsyncSession, org_id: UUID, vendor_id: UUID) -> None:
    vendor = await get_vendor(db, org_id, vendor_id)
    await db.delete(vendor)
    await db.commit()


async def create_assessment(
    db: AsyncSession, org_id: UUID, vendor_id: UUID, data: VendorAssessmentCreate,
    assessed_by_id: UUID | None = None,
) -> VendorAssessment:
    await get_vendor(db, org_id, vendor_id)
    assessment = VendorAssessment(
        vendor_id=vendor_id,
        org_id=org_id,
        assessed_by_id=assessed_by_id,
        **data.model_dump(),
    )
    db.add(assessment)

    # Update vendor's last assessment info
    vendor = await get_vendor(db, org_id, vendor_id)
    vendor.last_assessment_date = data.assessment_date or datetime.now(timezone.utc)
    if data.score is not None:
        vendor.assessment_score = data.score
    if data.risk_tier_assigned:
        vendor.risk_tier = data.risk_tier_assigned

    await db.commit()
    await db.refresh(assessment)
    return assessment


async def get_assessments(db: AsyncSession, org_id: UUID, vendor_id: UUID) -> list[VendorAssessment]:
    await get_vendor(db, org_id, vendor_id)
    result = await db.execute(
        select(VendorAssessment)
        .where(VendorAssessment.vendor_id == vendor_id, VendorAssessment.org_id == org_id)
        .order_by(VendorAssessment.created_at.desc())
    )
    return list(result.scalars().all())


async def get_vendor_stats(db: AsyncSession, org_id: UUID) -> dict:
    result = await db.execute(select(Vendor).where(Vendor.org_id == org_id))
    vendors = list(result.scalars().all())

    by_risk_tier: dict[str, int] = {}
    by_status: dict[str, int] = {}
    expiring = 0
    now = datetime.now(timezone.utc)
    threshold = now + timedelta(days=90)

    for v in vendors:
        by_risk_tier[v.risk_tier] = by_risk_tier.get(v.risk_tier, 0) + 1
        by_status[v.status] = by_status.get(v.status, 0) + 1
        if v.contract_end_date and v.contract_end_date <= threshold:
            expiring += 1

    return {
        "total": len(vendors),
        "by_risk_tier": by_risk_tier,
        "by_status": by_status,
        "expiring_contracts_count": expiring,
    }
