from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.incident import Incident, IncidentTimelineEvent
from app.schemas.incident import IncidentCreate, IncidentUpdate, TimelineEventCreate


async def list_incidents(
    db: AsyncSession,
    org_id: UUID,
    status: str | None = None,
    severity: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[Incident], int]:
    base_q = select(Incident).where(Incident.org_id == org_id)
    count_q = select(func.count()).select_from(Incident).where(Incident.org_id == org_id)

    if status:
        base_q = base_q.where(Incident.status == status)
        count_q = count_q.where(Incident.status == status)
    if severity:
        base_q = base_q.where(Incident.severity == severity)
        count_q = count_q.where(Incident.severity == severity)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(Incident.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_incident(db: AsyncSession, org_id: UUID, data: IncidentCreate) -> Incident:
    incident = Incident(org_id=org_id, **data.model_dump())
    db.add(incident)
    await db.commit()
    await db.refresh(incident)

    # Auto-create timeline event for creation
    event = IncidentTimelineEvent(
        incident_id=incident.id,
        event_type="created",
        description=f"Incident created with severity {data.severity}",
        occurred_at=datetime.now(timezone.utc),
    )
    db.add(event)
    await db.commit()
    await db.refresh(incident)
    return incident


async def get_incident(db: AsyncSession, org_id: UUID, incident_id: UUID) -> Incident:
    result = await db.execute(
        select(Incident).where(Incident.id == incident_id, Incident.org_id == org_id)
    )
    incident = result.scalar_one_or_none()
    if not incident:
        raise NotFoundError(f"Incident {incident_id} not found")
    return incident


async def update_incident(
    db: AsyncSession, org_id: UUID, incident_id: UUID, data: IncidentUpdate, actor_id: UUID | None = None
) -> Incident:
    incident = await get_incident(db, org_id, incident_id)
    update_data = data.model_dump(exclude_unset=True)
    old_status = incident.status

    for field, value in update_data.items():
        setattr(incident, field, value)

    # Auto-set resolved_at when status changes to resolved
    if "status" in update_data and update_data["status"] in ("resolved", "closed") and not incident.resolved_at:
        incident.resolved_at = datetime.now(timezone.utc)

    # Auto-create timeline event on status change
    if "status" in update_data and update_data["status"] != old_status:
        event = IncidentTimelineEvent(
            incident_id=incident.id,
            actor_id=actor_id,
            event_type="status_change",
            description=f"Status changed from {old_status} to {update_data['status']}",
            occurred_at=datetime.now(timezone.utc),
        )
        db.add(event)

    await db.commit()
    await db.refresh(incident)
    return incident


async def delete_incident(db: AsyncSession, org_id: UUID, incident_id: UUID) -> None:
    incident = await get_incident(db, org_id, incident_id)
    await db.delete(incident)
    await db.commit()


async def add_timeline_event(
    db: AsyncSession, org_id: UUID, incident_id: UUID, data: TimelineEventCreate, actor_id: UUID | None = None
) -> IncidentTimelineEvent:
    await get_incident(db, org_id, incident_id)
    event = IncidentTimelineEvent(
        incident_id=incident_id,
        actor_id=actor_id,
        event_type=data.event_type,
        description=data.description,
        occurred_at=data.occurred_at or datetime.now(timezone.utc),
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


async def get_timeline(db: AsyncSession, org_id: UUID, incident_id: UUID) -> list[IncidentTimelineEvent]:
    await get_incident(db, org_id, incident_id)
    result = await db.execute(
        select(IncidentTimelineEvent)
        .where(IncidentTimelineEvent.incident_id == incident_id)
        .order_by(IncidentTimelineEvent.occurred_at.desc())
    )
    return list(result.scalars().all())


async def get_incident_stats(db: AsyncSession, org_id: UUID) -> dict:
    result = await db.execute(select(Incident).where(Incident.org_id == org_id))
    incidents = list(result.scalars().all())

    by_status: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    open_p1 = 0
    resolution_hours: list[float] = []

    for inc in incidents:
        by_status[inc.status] = by_status.get(inc.status, 0) + 1
        by_severity[inc.severity] = by_severity.get(inc.severity, 0) + 1
        if inc.severity == "P1" and inc.status in ("open", "investigating"):
            open_p1 += 1
        if inc.resolved_at and inc.detected_at:
            delta = (inc.resolved_at - inc.detected_at).total_seconds() / 3600
            resolution_hours.append(delta)
        elif inc.resolved_at:
            delta = (inc.resolved_at - inc.created_at).total_seconds() / 3600
            resolution_hours.append(delta)

    return {
        "total": len(incidents),
        "by_status": by_status,
        "by_severity": by_severity,
        "open_p1_count": open_p1,
        "avg_resolution_hours": round(sum(resolution_hours) / len(resolution_hours), 1) if resolution_hours else 0.0,
    }
