"""Audit log service — records all entity changes for compliance tracking.

The AuditLog model already exists; this service provides the query and
creation API, plus a helper that API routes can call after mutations.
"""

import logging
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog

logger = logging.getLogger(__name__)


async def log_action(
    db: AsyncSession,
    org_id: UUID,
    actor_id: str,
    actor_type: str,
    action: str,
    entity_type: str,
    entity_id: str,
    changes: dict | None = None,
    ip_address: str | None = None,
) -> AuditLog:
    """Create an audit log entry. Called after every mutation."""
    entry = AuditLog(
        org_id=org_id,
        actor_id=str(actor_id),
        actor_type=actor_type,
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id),
        changes=changes,
        ip_address=ip_address,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(entry)
    # Don't commit here — let the caller's transaction handle it
    return entry


async def list_audit_logs(
    db: AsyncSession,
    org_id: UUID,
    entity_type: str | None = None,
    entity_id: str | None = None,
    actor_id: str | None = None,
    action: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[AuditLog], int]:
    base_q = select(AuditLog).where(AuditLog.org_id == org_id)
    count_q = select(func.count()).select_from(AuditLog).where(AuditLog.org_id == org_id)

    if entity_type:
        base_q = base_q.where(AuditLog.entity_type == entity_type)
        count_q = count_q.where(AuditLog.entity_type == entity_type)
    if entity_id:
        base_q = base_q.where(AuditLog.entity_id == entity_id)
        count_q = count_q.where(AuditLog.entity_id == entity_id)
    if actor_id:
        base_q = base_q.where(AuditLog.actor_id == actor_id)
        count_q = count_q.where(AuditLog.actor_id == actor_id)
    if action:
        base_q = base_q.where(AuditLog.action == action)
        count_q = count_q.where(AuditLog.action == action)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(
        AuditLog.timestamp.desc()
    )
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def get_audit_log_stats(db: AsyncSession, org_id: UUID) -> dict:
    result = await db.execute(select(AuditLog).where(AuditLog.org_id == org_id))
    logs = list(result.scalars().all())

    by_action: dict[str, int] = {}
    by_entity: dict[str, int] = {}
    for log in logs:
        by_action[log.action] = by_action.get(log.action, 0) + 1
        by_entity[log.entity_type] = by_entity.get(log.entity_type, 0) + 1

    return {
        "total": len(logs),
        "by_action": by_action,
        "by_entity_type": by_entity,
    }
