import hashlib
import secrets
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, UnauthorizedError
from app.models.audit import Audit
from app.models.auditor_access_token import AuditorAccessToken
from app.schemas.audit import TokenCreate


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


async def create_access_token(
    db: AsyncSession, org_id: UUID, audit_id: UUID, data: TokenCreate
) -> tuple[AuditorAccessToken, str]:
    """Create an access token and return (token_model, raw_token)."""
    # Verify audit
    result = await db.execute(
        select(Audit).where(Audit.id == audit_id, Audit.org_id == org_id)
    )
    if not result.scalar_one_or_none():
        raise NotFoundError(f"Audit {audit_id} not found")

    raw_token = secrets.token_urlsafe(48)
    token_hash = _hash_token(raw_token)

    access_token = AuditorAccessToken(
        audit_id=audit_id,
        token_hash=token_hash,
        auditor_email=data.auditor_email,
        auditor_name=data.auditor_name,
        permissions=data.permissions or {"read_all": True},
        expires_at=data.expires_at,
    )
    db.add(access_token)
    await db.commit()
    await db.refresh(access_token)
    return access_token, raw_token


async def validate_token(db: AsyncSession, raw_token: str) -> tuple[AuditorAccessToken, Audit]:
    """Validate a raw token and return the token + audit."""
    token_hash = _hash_token(raw_token)
    result = await db.execute(
        select(AuditorAccessToken).where(AuditorAccessToken.token_hash == token_hash)
    )
    access_token = result.scalar_one_or_none()

    if not access_token:
        raise UnauthorizedError("Invalid auditor access token")

    if not access_token.is_active:
        raise UnauthorizedError("Access token has been revoked")

    if access_token.expires_at < datetime.now(timezone.utc):
        raise UnauthorizedError("Access token has expired")

    # Get the audit
    audit_result = await db.execute(
        select(Audit).where(Audit.id == access_token.audit_id)
    )
    audit = audit_result.scalar_one_or_none()
    if not audit:
        raise UnauthorizedError("Associated audit not found")

    return access_token, audit


async def revoke_token(db: AsyncSession, org_id: UUID, audit_id: UUID, token_id: UUID) -> None:
    result = await db.execute(
        select(AuditorAccessToken).where(
            AuditorAccessToken.id == token_id,
            AuditorAccessToken.audit_id == audit_id,
        )
    )
    token = result.scalar_one_or_none()
    if not token:
        raise NotFoundError(f"Token {token_id} not found")
    token.is_active = False
    await db.commit()


async def list_tokens(db: AsyncSession, audit_id: UUID) -> list[AuditorAccessToken]:
    result = await db.execute(
        select(AuditorAccessToken).where(
            AuditorAccessToken.audit_id == audit_id
        ).order_by(AuditorAccessToken.created_at.desc())
    )
    return list(result.scalars().all())
