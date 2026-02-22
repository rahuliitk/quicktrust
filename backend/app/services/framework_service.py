from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundError
from app.models.framework import Framework
from app.models.framework_domain import FrameworkDomain
from app.models.framework_requirement import FrameworkRequirement


async def list_frameworks(db: AsyncSession) -> list[Framework]:
    result = await db.execute(
        select(Framework).where(Framework.is_active == True).order_by(Framework.name)
    )
    return list(result.scalars().all())


async def get_framework(db: AsyncSession, framework_id: UUID) -> Framework:
    result = await db.execute(
        select(Framework)
        .options(
            selectinload(Framework.domains)
            .selectinload(FrameworkDomain.requirements)
            .selectinload(FrameworkRequirement.objectives)
        )
        .where(Framework.id == framework_id)
    )
    framework = result.scalar_one_or_none()
    if not framework:
        raise NotFoundError(f"Framework {framework_id} not found")
    return framework


async def get_framework_domains(db: AsyncSession, framework_id: UUID) -> list[FrameworkDomain]:
    await get_framework(db, framework_id)  # Verify framework exists
    result = await db.execute(
        select(FrameworkDomain)
        .where(FrameworkDomain.framework_id == framework_id)
        .order_by(FrameworkDomain.sort_order)
    )
    return list(result.scalars().all())


async def get_domain(db: AsyncSession, domain_id: UUID) -> FrameworkDomain:
    result = await db.execute(
        select(FrameworkDomain)
        .options(selectinload(FrameworkDomain.requirements).selectinload(FrameworkRequirement.objectives))
        .where(FrameworkDomain.id == domain_id)
    )
    domain = result.scalar_one_or_none()
    if not domain:
        raise NotFoundError(f"Domain {domain_id} not found")
    return domain


async def get_requirements(
    db: AsyncSession, framework_id: UUID
) -> list[FrameworkRequirement]:
    result = await db.execute(
        select(FrameworkRequirement)
        .join(FrameworkDomain)
        .where(FrameworkDomain.framework_id == framework_id)
        .order_by(FrameworkRequirement.sort_order)
    )
    return list(result.scalars().all())


async def get_requirement(db: AsyncSession, requirement_id: UUID) -> FrameworkRequirement:
    result = await db.execute(
        select(FrameworkRequirement)
        .options(selectinload(FrameworkRequirement.objectives))
        .where(FrameworkRequirement.id == requirement_id)
    )
    req = result.scalar_one_or_none()
    if not req:
        raise NotFoundError(f"Requirement {requirement_id} not found")
    return req
