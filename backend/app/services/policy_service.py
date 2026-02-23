from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.policy import Policy
from app.models.policy_template import PolicyTemplate
from app.schemas.policy import PolicyCreate, PolicyUpdate, PolicyStatsResponse


async def list_policies(
    db: AsyncSession,
    org_id: UUID,
    status: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[Policy], int]:
    base_q = select(Policy).where(Policy.org_id == org_id)
    count_base = select(func.count()).select_from(Policy).where(Policy.org_id == org_id)

    if status:
        base_q = base_q.where(Policy.status == status)
        count_base = count_base.where(Policy.status == status)

    total = (await db.execute(count_base)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(Policy.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_policy(db: AsyncSession, org_id: UUID, data: PolicyCreate) -> Policy:
    policy = Policy(org_id=org_id, **data.model_dump())
    db.add(policy)
    await db.commit()
    await db.refresh(policy)
    return policy


async def get_policy(db: AsyncSession, org_id: UUID, policy_id: UUID) -> Policy:
    result = await db.execute(
        select(Policy).where(Policy.id == policy_id, Policy.org_id == org_id)
    )
    policy = result.scalar_one_or_none()
    if not policy:
        raise NotFoundError(f"Policy {policy_id} not found")
    return policy


async def update_policy(
    db: AsyncSession, org_id: UUID, policy_id: UUID, data: PolicyUpdate
) -> Policy:
    policy = await get_policy(db, org_id, policy_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(policy, field, value)
    await db.commit()
    await db.refresh(policy)
    return policy


async def delete_policy(db: AsyncSession, org_id: UUID, policy_id: UUID) -> None:
    policy = await get_policy(db, org_id, policy_id)
    await db.delete(policy)
    await db.commit()


async def get_policy_stats(db: AsyncSession, org_id: UUID) -> PolicyStatsResponse:
    result = await db.execute(
        select(
            func.count().label("total"),
            func.count().filter(Policy.status == "draft").label("draft"),
            func.count().filter(Policy.status == "in_review").label("in_review"),
            func.count().filter(Policy.status == "approved").label("approved"),
            func.count().filter(Policy.status == "published").label("published"),
            func.count().filter(Policy.status == "archived").label("archived"),
        )
        .select_from(Policy)
        .where(Policy.org_id == org_id)
    )
    row = result.one()
    return PolicyStatsResponse(
        total=row.total,
        draft=row.draft,
        in_review=row.in_review,
        approved=row.approved,
        published=row.published,
        archived=row.archived,
    )


async def list_policy_templates(
    db: AsyncSession,
    category: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[PolicyTemplate], int]:
    base_q = select(PolicyTemplate)
    count_base = select(func.count()).select_from(PolicyTemplate)

    if category:
        base_q = base_q.where(PolicyTemplate.category == category)
        count_base = count_base.where(PolicyTemplate.category == category)

    total = (await db.execute(count_base)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(PolicyTemplate.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def get_policy_template(db: AsyncSession, template_id: UUID) -> PolicyTemplate:
    result = await db.execute(
        select(PolicyTemplate).where(PolicyTemplate.id == template_id)
    )
    template = result.scalar_one_or_none()
    if not template:
        raise NotFoundError(f"Policy template {template_id} not found")
    return template
