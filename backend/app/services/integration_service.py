from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.integration import Integration
from app.schemas.integration import IntegrationCreate, IntegrationUpdate


async def list_integrations(
    db: AsyncSession, org_id: UUID, page: int = 1, page_size: int = 50
) -> tuple[list[Integration], int]:
    base_q = select(Integration).where(Integration.org_id == org_id)
    count_q = select(func.count()).select_from(Integration).where(Integration.org_id == org_id)
    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(Integration.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_integration(db: AsyncSession, org_id: UUID, data: IntegrationCreate) -> Integration:
    integration = Integration(org_id=org_id, **data.model_dump())
    db.add(integration)
    await db.commit()
    await db.refresh(integration)
    return integration


async def get_integration(db: AsyncSession, org_id: UUID, integration_id: UUID) -> Integration:
    result = await db.execute(
        select(Integration).where(
            Integration.id == integration_id, Integration.org_id == org_id
        )
    )
    integration = result.scalar_one_or_none()
    if not integration:
        raise NotFoundError(f"Integration {integration_id} not found")
    return integration


async def update_integration(
    db: AsyncSession, org_id: UUID, integration_id: UUID, data: IntegrationUpdate
) -> Integration:
    integration = await get_integration(db, org_id, integration_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(integration, key, value)
    await db.commit()
    await db.refresh(integration)
    return integration


async def delete_integration(db: AsyncSession, org_id: UUID, integration_id: UUID) -> None:
    integration = await get_integration(db, org_id, integration_id)
    await db.delete(integration)
    await db.commit()
