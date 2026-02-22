from uuid import UUID

from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.control import Control
from app.schemas.control import ControlCreate, ControlUpdate, ControlStatsResponse


async def list_controls(
    db: AsyncSession,
    org_id: UUID,
    status: str | None = None,
    framework_id: UUID | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[Control], int]:
    base_q = select(Control).where(Control.org_id == org_id)
    count_base = select(func.count()).select_from(Control).where(Control.org_id == org_id)

    if status:
        base_q = base_q.where(Control.status == status)
        count_base = count_base.where(Control.status == status)

    total = (await db.execute(count_base)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(Control.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_control(db: AsyncSession, org_id: UUID, data: ControlCreate) -> Control:
    control = Control(org_id=org_id, **data.model_dump())
    db.add(control)
    await db.commit()
    await db.refresh(control)
    return control


async def get_control(db: AsyncSession, org_id: UUID, control_id: UUID) -> Control:
    result = await db.execute(
        select(Control).where(Control.id == control_id, Control.org_id == org_id)
    )
    control = result.scalar_one_or_none()
    if not control:
        raise NotFoundError(f"Control {control_id} not found")
    return control


async def update_control(
    db: AsyncSession, org_id: UUID, control_id: UUID, data: ControlUpdate
) -> Control:
    control = await get_control(db, org_id, control_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(control, field, value)
    await db.commit()
    await db.refresh(control)
    return control


async def delete_control(db: AsyncSession, org_id: UUID, control_id: UUID) -> None:
    control = await get_control(db, org_id, control_id)
    await db.delete(control)
    await db.commit()


async def bulk_approve_controls(
    db: AsyncSession, org_id: UUID, control_ids: list[UUID], status: str = "implemented"
) -> int:
    count = 0
    for cid in control_ids:
        result = await db.execute(
            select(Control).where(Control.id == cid, Control.org_id == org_id)
        )
        control = result.scalar_one_or_none()
        if control:
            control.status = status
            count += 1
    await db.commit()
    return count


async def get_control_stats(db: AsyncSession, org_id: UUID) -> ControlStatsResponse:
    result = await db.execute(
        select(
            func.count().label("total"),
            func.count().filter(Control.status == "draft").label("draft"),
            func.count().filter(Control.status == "implemented").label("implemented"),
            func.count().filter(Control.status == "partially_implemented").label("partially_implemented"),
            func.count().filter(Control.status == "not_implemented").label("not_implemented"),
            func.count().filter(Control.status == "not_applicable").label("not_applicable"),
        )
        .select_from(Control)
        .where(Control.org_id == org_id)
    )
    row = result.one()
    return ControlStatsResponse(
        total=row.total,
        draft=row.draft,
        implemented=row.implemented,
        partially_implemented=row.partially_implemented,
        not_implemented=row.not_implemented,
        not_applicable=row.not_applicable,
    )
