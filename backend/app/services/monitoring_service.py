from datetime import datetime, timezone, timedelta
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.monitoring import MonitorRule, MonitorAlert
from app.models.evidence import Evidence
from app.models.control import Control
from app.models.policy import Policy
from app.schemas.monitoring import MonitorRuleCreate, MonitorRuleUpdate, MonitorAlertUpdate


# === Rules ===

async def list_rules(
    db: AsyncSession,
    org_id: UUID,
    check_type: str | None = None,
    is_active: bool | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[MonitorRule], int]:
    base_q = select(MonitorRule).where(MonitorRule.org_id == org_id)
    count_q = select(func.count()).select_from(MonitorRule).where(MonitorRule.org_id == org_id)

    if check_type:
        base_q = base_q.where(MonitorRule.check_type == check_type)
        count_q = count_q.where(MonitorRule.check_type == check_type)
    if is_active is not None:
        base_q = base_q.where(MonitorRule.is_active == is_active)
        count_q = count_q.where(MonitorRule.is_active == is_active)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(MonitorRule.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_rule(db: AsyncSession, org_id: UUID, data: MonitorRuleCreate) -> MonitorRule:
    rule = MonitorRule(org_id=org_id, **data.model_dump())
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule


async def get_rule(db: AsyncSession, org_id: UUID, rule_id: UUID) -> MonitorRule:
    result = await db.execute(
        select(MonitorRule).where(MonitorRule.id == rule_id, MonitorRule.org_id == org_id)
    )
    rule = result.scalar_one_or_none()
    if not rule:
        raise NotFoundError(f"Monitor rule {rule_id} not found")
    return rule


async def update_rule(
    db: AsyncSession, org_id: UUID, rule_id: UUID, data: MonitorRuleUpdate
) -> MonitorRule:
    rule = await get_rule(db, org_id, rule_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(rule, field, value)
    await db.commit()
    await db.refresh(rule)
    return rule


async def delete_rule(db: AsyncSession, org_id: UUID, rule_id: UUID) -> None:
    rule = await get_rule(db, org_id, rule_id)
    await db.delete(rule)
    await db.commit()


async def run_checks(db: AsyncSession, org_id: UUID, rule_id: UUID) -> list[MonitorAlert]:
    """Run checks for a specific rule and create alerts for failures."""
    rule = await get_rule(db, org_id, rule_id)
    now = datetime.now(timezone.utc)
    alerts_created: list[MonitorAlert] = []

    if rule.check_type == "evidence_staleness":
        staleness_days = (rule.config or {}).get("staleness_days", 90)
        threshold = now - timedelta(days=staleness_days)
        result = await db.execute(
            select(Evidence).where(
                Evidence.org_id == org_id,
                Evidence.collected_at < threshold,
            )
        )
        stale = list(result.scalars().all())
        if stale:
            alert = MonitorAlert(
                org_id=org_id,
                rule_id=rule.id,
                severity="high",
                title=f"{len(stale)} evidence items are stale (>{staleness_days} days)",
                details={"stale_count": len(stale), "evidence_ids": [str(e.id) for e in stale[:10]]},
                triggered_at=now,
            )
            db.add(alert)
            alerts_created.append(alert)
            rule.last_result = "fail"
        else:
            rule.last_result = "pass"

    elif rule.check_type == "control_status":
        result = await db.execute(
            select(Control).where(
                Control.org_id == org_id,
                Control.status.in_(["not_implemented", "draft"]),
            )
        )
        failing = list(result.scalars().all())
        if failing:
            alert = MonitorAlert(
                org_id=org_id,
                rule_id=rule.id,
                severity="medium",
                title=f"{len(failing)} controls are not implemented",
                details={"failing_count": len(failing)},
                triggered_at=now,
            )
            db.add(alert)
            alerts_created.append(alert)
            rule.last_result = "fail"
        else:
            rule.last_result = "pass"

    elif rule.check_type == "policy_expiry":
        result = await db.execute(
            select(Policy).where(
                Policy.org_id == org_id,
                Policy.next_review_date < now,
            )
        )
        expired = list(result.scalars().all())
        if expired:
            alert = MonitorAlert(
                org_id=org_id,
                rule_id=rule.id,
                severity="high",
                title=f"{len(expired)} policies are past their review date",
                details={"expired_count": len(expired)},
                triggered_at=now,
            )
            db.add(alert)
            alerts_created.append(alert)
            rule.last_result = "fail"
        else:
            rule.last_result = "pass"
    else:
        rule.last_result = "pass"

    rule.last_checked_at = now
    await db.commit()
    for a in alerts_created:
        await db.refresh(a)
    return alerts_created


# === Alerts ===

async def list_alerts(
    db: AsyncSession,
    org_id: UUID,
    status: str | None = None,
    severity: str | None = None,
    rule_id: UUID | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[MonitorAlert], int]:
    base_q = select(MonitorAlert).where(MonitorAlert.org_id == org_id)
    count_q = select(func.count()).select_from(MonitorAlert).where(MonitorAlert.org_id == org_id)

    if status:
        base_q = base_q.where(MonitorAlert.status == status)
        count_q = count_q.where(MonitorAlert.status == status)
    if severity:
        base_q = base_q.where(MonitorAlert.severity == severity)
        count_q = count_q.where(MonitorAlert.severity == severity)
    if rule_id:
        base_q = base_q.where(MonitorAlert.rule_id == rule_id)
        count_q = count_q.where(MonitorAlert.rule_id == rule_id)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(MonitorAlert.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def update_alert(
    db: AsyncSession, org_id: UUID, alert_id: UUID, data: MonitorAlertUpdate,
    user_id: UUID | None = None,
) -> MonitorAlert:
    result = await db.execute(
        select(MonitorAlert).where(MonitorAlert.id == alert_id, MonitorAlert.org_id == org_id)
    )
    alert = result.scalar_one_or_none()
    if not alert:
        raise NotFoundError(f"Alert {alert_id} not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(alert, field, value)

    if "status" in update_data:
        if update_data["status"] == "acknowledged":
            alert.acknowledged_by_id = user_id
        elif update_data["status"] == "resolved":
            alert.resolved_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(alert)
    return alert


# === Stats ===

async def get_monitoring_stats(db: AsyncSession, org_id: UUID) -> dict:
    rules_result = await db.execute(select(MonitorRule).where(MonitorRule.org_id == org_id))
    rules = list(rules_result.scalars().all())

    alerts_result = await db.execute(
        select(MonitorAlert).where(MonitorAlert.org_id == org_id, MonitorAlert.status == "open")
    )
    open_alerts = list(alerts_result.scalars().all())

    by_severity: dict[str, int] = {}
    for a in open_alerts:
        by_severity[a.severity] = by_severity.get(a.severity, 0) + 1

    return {
        "total_rules": len(rules),
        "active_rules": sum(1 for r in rules if r.is_active),
        "open_alerts": len(open_alerts),
        "by_severity": by_severity,
    }
