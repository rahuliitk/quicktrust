"""Notification service — in-app, email, and Slack notifications.

Sends notifications through configured channels with graceful degradation.
"""

import logging
from datetime import datetime, timezone
from uuid import UUID

import httpx
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.notification import Notification, SlackWebhookConfig
from app.schemas.notification import NotificationCreate

logger = logging.getLogger(__name__)


async def create_notification(
    db: AsyncSession, org_id: UUID, data: NotificationCreate
) -> Notification:
    """Create an in-app notification and optionally dispatch to external channels."""
    notification = Notification(
        org_id=org_id,
        user_id=data.user_id,
        channel=data.channel,
        category=data.category,
        title=data.title,
        message=data.message,
        severity=data.severity,
        entity_type=data.entity_type,
        entity_id=data.entity_id,
        sent_at=datetime.now(timezone.utc),
    )
    db.add(notification)
    await db.commit()
    await db.refresh(notification)

    # Fire-and-forget external delivery
    if data.channel in ("slack", "all"):
        await _send_slack(db, org_id, notification)
    if data.channel in ("email", "all"):
        await _send_email(notification)

    return notification


async def send_system_notification(
    db: AsyncSession,
    org_id: UUID,
    category: str,
    title: str,
    message: str,
    severity: str = "info",
    entity_type: str | None = None,
    entity_id: str | None = None,
    user_id: UUID | None = None,
) -> Notification:
    """Helper for internal code to create notifications without building schemas."""
    data = NotificationCreate(
        channel="in_app",
        category=category,
        title=title,
        message=message,
        severity=severity,
        entity_type=entity_type,
        entity_id=str(entity_id) if entity_id else None,
        user_id=user_id,
    )
    return await create_notification(db, org_id, data)


async def list_notifications(
    db: AsyncSession,
    org_id: UUID,
    user_id: UUID | None = None,
    is_read: bool | None = None,
    category: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[Notification], int]:
    base_q = select(Notification).where(Notification.org_id == org_id)
    count_q = select(func.count()).select_from(Notification).where(Notification.org_id == org_id)

    if user_id:
        base_q = base_q.where(
            (Notification.user_id == user_id) | (Notification.user_id.is_(None))
        )
        count_q = count_q.where(
            (Notification.user_id == user_id) | (Notification.user_id.is_(None))
        )
    if is_read is not None:
        base_q = base_q.where(Notification.is_read == is_read)
        count_q = count_q.where(Notification.is_read == is_read)
    if category:
        base_q = base_q.where(Notification.category == category)
        count_q = count_q.where(Notification.category == category)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(
        Notification.created_at.desc()
    )
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def get_notification(
    db: AsyncSession, org_id: UUID, notification_id: UUID
) -> Notification:
    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id, Notification.org_id == org_id
        )
    )
    n = result.scalar_one_or_none()
    if not n:
        raise NotFoundError(f"Notification {notification_id} not found")
    return n


async def mark_read(
    db: AsyncSession, org_id: UUID, notification_id: UUID
) -> Notification:
    n = await get_notification(db, org_id, notification_id)
    n.is_read = True
    n.read_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(n)
    return n


async def mark_all_read(db: AsyncSession, org_id: UUID, user_id: UUID | None = None) -> int:
    stmt = (
        update(Notification)
        .where(Notification.org_id == org_id, Notification.is_read == False)  # noqa: E712
    )
    if user_id:
        stmt = stmt.where(
            (Notification.user_id == user_id) | (Notification.user_id.is_(None))
        )
    stmt = stmt.values(is_read=True, read_at=datetime.now(timezone.utc))
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount


async def get_notification_stats(
    db: AsyncSession, org_id: UUID, user_id: UUID | None = None
) -> dict:
    base = select(Notification).where(Notification.org_id == org_id)
    if user_id:
        base = base.where(
            (Notification.user_id == user_id) | (Notification.user_id.is_(None))
        )
    result = await db.execute(base)
    notifications = list(result.scalars().all())

    by_category: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    unread = 0
    for n in notifications:
        by_category[n.category] = by_category.get(n.category, 0) + 1
        by_severity[n.severity] = by_severity.get(n.severity, 0) + 1
        if not n.is_read:
            unread += 1

    return {
        "total": len(notifications),
        "unread": unread,
        "by_category": by_category,
        "by_severity": by_severity,
    }


# --- Slack webhook ---

async def configure_slack(
    db: AsyncSession, org_id: UUID, webhook_url: str,
    channel_name: str | None = None, categories: list[str] | None = None,
) -> SlackWebhookConfig:
    config = SlackWebhookConfig(
        org_id=org_id,
        webhook_url=webhook_url,
        channel_name=channel_name,
        categories=categories,
    )
    db.add(config)
    await db.commit()
    await db.refresh(config)
    return config


async def get_slack_config(db: AsyncSession, org_id: UUID) -> SlackWebhookConfig | None:
    result = await db.execute(
        select(SlackWebhookConfig).where(
            SlackWebhookConfig.org_id == org_id, SlackWebhookConfig.is_active == True  # noqa: E712
        )
    )
    return result.scalar_one_or_none()


async def _send_slack(db: AsyncSession, org_id: UUID, notification: Notification) -> None:
    config = await get_slack_config(db, org_id)
    if not config:
        return

    severity_emoji = {"info": ":information_source:", "warning": ":warning:", "critical": ":rotating_light:"}.get(
        notification.severity, ":bell:"
    )

    payload = {
        "text": f"{severity_emoji} *{notification.title}*\n{notification.message}",
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(config.webhook_url, json=payload)
            if resp.status_code != 200:
                logger.warning("Slack webhook returned %d: %s", resp.status_code, resp.text)
    except Exception as exc:
        logger.warning("Failed to send Slack notification: %s", exc)


async def _send_email(notification: Notification) -> None:
    """Send email notification via SMTP. Falls back to logging when SMTP is not configured."""
    from app.config import get_settings
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    settings = get_settings()
    if not settings.SMTP_HOST:
        logger.info(
            "EMAIL notification [%s]: %s — %s (SMTP not configured)",
            notification.severity,
            notification.title,
            notification.message,
        )
        return

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[{notification.severity.upper()}] {notification.title}"
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = settings.SMTP_FROM_EMAIL  # default; per-user routing can be added

        body = f"""
        <h2>{notification.title}</h2>
        <p>{notification.message}</p>
        <p><small>Severity: {notification.severity} | Category: {notification.category}</small></p>
        """
        msg.attach(MIMEText(body, "html"))

        if settings.SMTP_USE_TLS:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            server.starttls()
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)

        if settings.SMTP_USER:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        server.sendmail(settings.SMTP_FROM_EMAIL, [msg["To"]], msg.as_string())
        server.quit()
        logger.info("Email sent for notification %s", notification.id)
    except Exception as exc:
        logger.warning("Failed to send email notification: %s", exc)
