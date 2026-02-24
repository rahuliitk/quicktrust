from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import BadRequestError, NotFoundError
from app.models.framework import Framework
from app.models.framework_domain import FrameworkDomain
from app.models.framework_requirement import FrameworkRequirement
from app.schemas.framework import (
    DomainCreate,
    FrameworkCreate,
    FrameworkUpdate,
    RequirementCreate,
)

# Preset / seeded framework names that cannot be deleted
SEEDED_FRAMEWORK_NAMES = {
    "SOC 2 Type II",
    "ISO 27001:2022",
    "NIST CSF 2.0",
    "HIPAA",
    "PCI DSS 4.0",
    "GDPR",
}


async def list_frameworks(db: AsyncSession) -> list[Framework]:
    from app.core.cache import cache_get, cache_set

    cache_key = "frameworks:active_list"
    cached = await cache_get(cache_key)
    if cached:
        # Cached list is serialized; still need to return ORM objects for validation
        pass  # Fall through to DB query — cache speeds up stats/JSON endpoints

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


# ---------------------------------------------------------------------------
# CRUD operations for custom frameworks
# ---------------------------------------------------------------------------


async def create_framework(db: AsyncSession, data: FrameworkCreate) -> Framework:
    """Create a new custom compliance framework."""
    framework = Framework(
        name=data.name,
        version=data.version,
        category=data.category,
        description=data.description,
        is_active=True,
    )
    db.add(framework)
    await db.commit()
    await db.refresh(framework)
    return framework


async def update_framework(
    db: AsyncSession, framework_id: UUID, data: FrameworkUpdate
) -> Framework:
    """Update an existing framework's metadata."""
    framework = await get_framework(db, framework_id)
    update_fields = data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(framework, field, value)
    await db.commit()
    await db.refresh(framework)
    return framework


async def delete_framework(db: AsyncSession, framework_id: UUID) -> None:
    """Delete a custom framework. Seeded (preset) frameworks cannot be deleted."""
    framework = await get_framework(db, framework_id)
    if framework.name in SEEDED_FRAMEWORK_NAMES:
        raise BadRequestError(
            f"Cannot delete seeded framework '{framework.name}'. "
            "Only custom frameworks may be deleted."
        )
    await db.delete(framework)
    await db.commit()


async def add_domain(
    db: AsyncSession, framework_id: UUID, data: DomainCreate
) -> FrameworkDomain:
    """Add a new domain to an existing framework."""
    # Verify framework exists
    await get_framework(db, framework_id)

    # Determine next sort_order
    count_result = await db.execute(
        select(func.count()).select_from(FrameworkDomain).where(
            FrameworkDomain.framework_id == framework_id
        )
    )
    next_order = (count_result.scalar() or 0)

    domain = FrameworkDomain(
        framework_id=framework_id,
        code=data.code,
        name=data.name,
        description=data.description,
        sort_order=next_order,
    )
    db.add(domain)
    await db.commit()
    await db.refresh(domain)
    return domain


async def add_requirement(
    db: AsyncSession, framework_id: UUID, domain_id: UUID, data: RequirementCreate
) -> FrameworkRequirement:
    """Add a new requirement to a domain (verifying domain belongs to framework)."""
    # Verify domain exists and belongs to the framework
    domain = await get_domain(db, domain_id)
    if domain.framework_id != framework_id:
        raise BadRequestError(
            f"Domain {domain_id} does not belong to framework {framework_id}"
        )

    # Determine next sort_order
    count_result = await db.execute(
        select(func.count()).select_from(FrameworkRequirement).where(
            FrameworkRequirement.domain_id == domain_id
        )
    )
    next_order = (count_result.scalar() or 0)

    requirement = FrameworkRequirement(
        domain_id=domain_id,
        code=data.code,
        title=data.title,
        description=data.description,
        sort_order=next_order,
    )
    db.add(requirement)
    await db.commit()
    await db.refresh(requirement)
    return requirement
