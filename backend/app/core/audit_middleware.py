"""Lightweight audit-logging helper for API routes.

Instead of a heavy middleware that intercepts all requests, we provide a
dependency that routes can use to log actions after mutations. This approach
is explicit, testable, and doesn't require parsing request/response bodies.

Usage in a route:
    from app.core.audit_middleware import log_audit

    @router.post(...)
    async def create_something(..., db: DB, current_user: AnyInternalUser):
        item = await service.create(db, org_id, data)
        await log_audit(db, current_user, "create", "control", str(item.id), org_id)
        return item
"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.audit_log_service import log_action


async def log_audit(
    db: AsyncSession,
    user: User,
    action: str,
    entity_type: str,
    entity_id: str,
    org_id: UUID | None = None,
    changes: dict | None = None,
    ip_address: str | None = None,
) -> None:
    """Fire-and-forget audit log entry.

    Does not raise — errors are logged and swallowed so that audit
    logging failures never break business logic.
    """
    import logging

    try:
        await log_action(
            db=db,
            org_id=org_id or user.org_id,
            actor_id=str(user.id),
            actor_type="user",
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            changes=changes,
            ip_address=ip_address,
        )
    except Exception as exc:
        logging.getLogger(__name__).warning(
            "Failed to write audit log for %s %s: %s", action, entity_type, exc
        )
