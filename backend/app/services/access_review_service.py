from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.access_review import AccessReviewCampaign, AccessReviewEntry
from app.schemas.access_review import (
    AccessReviewCampaignCreate, AccessReviewCampaignUpdate,
    AccessReviewEntryCreate, AccessReviewEntryUpdate,
)


# === Campaigns ===

async def list_campaigns(
    db: AsyncSession,
    org_id: UUID,
    status: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[dict], int]:
    base_q = select(AccessReviewCampaign).where(AccessReviewCampaign.org_id == org_id)
    count_q = select(func.count()).select_from(AccessReviewCampaign).where(AccessReviewCampaign.org_id == org_id)

    if status:
        base_q = base_q.where(AccessReviewCampaign.status == status)
        count_q = count_q.where(AccessReviewCampaign.status == status)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(AccessReviewCampaign.created_at.desc())
    result = await db.execute(q)
    campaigns = list(result.scalars().all())

    # Enrich with entry counts
    enriched = []
    for c in campaigns:
        entry_count = len(c.entries) if c.entries else 0
        pending_count = sum(1 for e in (c.entries or []) if e.decision is None)
        enriched.append({
            **{col: getattr(c, col) for col in c.__table__.columns.keys()},
            "entry_count": entry_count,
            "pending_count": pending_count,
        })

    return enriched, total


async def create_campaign(db: AsyncSession, org_id: UUID, data: AccessReviewCampaignCreate) -> AccessReviewCampaign:
    campaign = AccessReviewCampaign(org_id=org_id, **data.model_dump())
    db.add(campaign)
    await db.commit()
    await db.refresh(campaign)
    return campaign


async def get_campaign(db: AsyncSession, org_id: UUID, campaign_id: UUID) -> AccessReviewCampaign:
    result = await db.execute(
        select(AccessReviewCampaign).where(
            AccessReviewCampaign.id == campaign_id, AccessReviewCampaign.org_id == org_id
        )
    )
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise NotFoundError(f"Access review campaign {campaign_id} not found")
    return campaign


async def get_campaign_response(db: AsyncSession, org_id: UUID, campaign_id: UUID) -> dict:
    campaign = await get_campaign(db, org_id, campaign_id)
    entry_count = len(campaign.entries) if campaign.entries else 0
    pending_count = sum(1 for e in (campaign.entries or []) if e.decision is None)
    return {
        **{col: getattr(campaign, col) for col in campaign.__table__.columns.keys()},
        "entry_count": entry_count,
        "pending_count": pending_count,
    }


async def update_campaign(
    db: AsyncSession, org_id: UUID, campaign_id: UUID, data: AccessReviewCampaignUpdate
) -> AccessReviewCampaign:
    campaign = await get_campaign(db, org_id, campaign_id)
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(campaign, field, value)

    # Auto-set completed_at
    if "status" in update_data and update_data["status"] == "completed" and not campaign.completed_at:
        campaign.completed_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(campaign)
    return campaign


async def delete_campaign(db: AsyncSession, org_id: UUID, campaign_id: UUID) -> None:
    campaign = await get_campaign(db, org_id, campaign_id)
    await db.delete(campaign)
    await db.commit()


# === Entries ===

async def list_entries(
    db: AsyncSession, org_id: UUID, campaign_id: UUID, decision: str | None = None
) -> list[AccessReviewEntry]:
    await get_campaign(db, org_id, campaign_id)
    q = select(AccessReviewEntry).where(
        AccessReviewEntry.campaign_id == campaign_id,
        AccessReviewEntry.org_id == org_id,
    )
    if decision:
        if decision == "pending":
            q = q.where(AccessReviewEntry.decision.is_(None))
        else:
            q = q.where(AccessReviewEntry.decision == decision)

    q = q.order_by(AccessReviewEntry.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all())


async def create_entry(
    db: AsyncSession, org_id: UUID, campaign_id: UUID, data: AccessReviewEntryCreate
) -> AccessReviewEntry:
    await get_campaign(db, org_id, campaign_id)
    entry = AccessReviewEntry(
        campaign_id=campaign_id,
        org_id=org_id,
        **data.model_dump(),
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


async def update_entry(
    db: AsyncSession, org_id: UUID, campaign_id: UUID, entry_id: UUID,
    data: AccessReviewEntryUpdate, decided_by_id: UUID | None = None,
) -> AccessReviewEntry:
    await get_campaign(db, org_id, campaign_id)
    result = await db.execute(
        select(AccessReviewEntry).where(
            AccessReviewEntry.id == entry_id,
            AccessReviewEntry.campaign_id == campaign_id,
        )
    )
    entry = result.scalar_one_or_none()
    if not entry:
        raise NotFoundError(f"Entry {entry_id} not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(entry, field, value)

    # Auto-set decided_at and decided_by when decision is set
    if "decision" in update_data and update_data["decision"] is not None:
        entry.decided_at = datetime.now(timezone.utc)
        entry.decided_by_id = decided_by_id

    await db.commit()
    await db.refresh(entry)
    return entry


# === Stats ===

async def get_access_review_stats(db: AsyncSession, org_id: UUID) -> dict:
    campaigns_result = await db.execute(
        select(AccessReviewCampaign).where(AccessReviewCampaign.org_id == org_id)
    )
    campaigns = list(campaigns_result.scalars().all())

    entries_result = await db.execute(
        select(AccessReviewEntry).where(AccessReviewEntry.org_id == org_id)
    )
    entries = list(entries_result.scalars().all())

    return {
        "total_campaigns": len(campaigns),
        "active_campaigns": sum(1 for c in campaigns if c.status == "active"),
        "total_entries": len(entries),
        "pending_decisions": sum(1 for e in entries if e.decision is None),
        "approved": sum(1 for e in entries if e.decision == "approved"),
        "revoked": sum(1 for e in entries if e.decision == "revoked"),
    }
