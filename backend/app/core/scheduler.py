"""APScheduler integration for periodic monitoring checks.

The scheduler reads all active ``MonitorRule`` rows from the database and
creates APScheduler jobs that invoke ``monitoring_service.run_checks`` on the
configured schedule (hourly / daily / weekly).
"""

from __future__ import annotations

import logging
from uuid import UUID

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

# Mapping from MonitorRule.schedule values to APScheduler trigger kwargs
_SCHEDULE_MAP: dict[str, dict] = {
    "hourly": {"trigger": "interval", "hours": 1},
    "daily": {"trigger": "interval", "hours": 24},
    "weekly": {"trigger": "interval", "weeks": 1},
}


async def start_scheduler() -> None:
    """Start the scheduler and load all active monitoring rules as jobs."""
    try:
        from app.core.database import async_session

        async with async_session() as db:
            await sync_monitoring_rules(db)

        scheduler.start()
        logger.info("APScheduler started with monitoring jobs.")
    except Exception as exc:
        logger.warning("Failed to start scheduler: %s. Monitoring jobs will be disabled.", exc)


async def stop_scheduler() -> None:
    """Gracefully shut down the scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler stopped.")


async def sync_monitoring_rules(db) -> None:
    """Read all active monitoring rules and create/update APScheduler jobs.

    Existing jobs whose rule has been deactivated or deleted are removed.
    """
    from app.models.monitoring import MonitorRule

    result = await db.execute(
        select(MonitorRule).where(MonitorRule.is_active.is_(True))
    )
    active_rules = list(result.scalars().all())

    active_job_ids: set[str] = set()

    for rule in active_rules:
        job_id = f"monitor_rule_{rule.id}"
        active_job_ids.add(job_id)

        schedule_kwargs = _SCHEDULE_MAP.get(rule.schedule, _SCHEDULE_MAP["daily"]).copy()
        trigger = schedule_kwargs.pop("trigger")

        existing_job = scheduler.get_job(job_id)
        if existing_job:
            # Reschedule in case the interval changed
            existing_job.reschedule(trigger=trigger, **schedule_kwargs)
            logger.debug("Rescheduled job %s", job_id)
        else:
            scheduler.add_job(
                _run_monitoring_check,
                trigger=trigger,
                id=job_id,
                args=[str(rule.org_id), str(rule.id)],
                replace_existing=True,
                **schedule_kwargs,
            )
            logger.info("Added monitoring job %s (schedule=%s)", job_id, rule.schedule)

    # Remove jobs for rules that are no longer active
    for job in scheduler.get_jobs():
        if job.id.startswith("monitor_rule_") and job.id not in active_job_ids:
            scheduler.remove_job(job.id)
            logger.info("Removed stale monitoring job %s", job.id)


async def _run_monitoring_check(org_id: str, rule_id: str) -> None:
    """Callback executed by APScheduler: opens a DB session and runs checks."""
    from app.core.database import async_session
    from app.services import monitoring_service

    try:
        async with async_session() as db:
            alerts = await monitoring_service.run_checks(
                db, UUID(org_id), UUID(rule_id)
            )
            if alerts:
                logger.info(
                    "Monitoring rule %s generated %d alert(s)", rule_id, len(alerts)
                )
            else:
                logger.debug("Monitoring rule %s passed.", rule_id)
    except Exception as exc:
        logger.error("Error running monitoring check for rule %s: %s", rule_id, exc)
