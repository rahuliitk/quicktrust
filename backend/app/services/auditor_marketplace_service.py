"""Auditor registration and marketplace discovery."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import BadRequestError, NotFoundError
from app.models.auditor_profile import AuditorProfile
from app.models.user import User
from app.schemas.auditor_profile import AuditorProfileCreate, AuditorProfileUpdate


async def register_auditor(
    db: AsyncSession, user_id: UUID, data: AuditorProfileCreate
) -> AuditorProfile:
    """Create an auditor profile for a user."""
    # Check if profile already exists
    existing = await db.execute(
        select(AuditorProfile).where(AuditorProfile.user_id == user_id)
    )
    if existing.scalar_one_or_none():
        raise BadRequestError("Auditor profile already exists for this user")

    profile = AuditorProfile(user_id=user_id, **data.model_dump())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


async def update_profile(
    db: AsyncSession, user_id: UUID, data: AuditorProfileUpdate
) -> AuditorProfile:
    profile = await _get_profile_by_user(db, user_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    await db.commit()
    await db.refresh(profile)
    return profile


async def get_profile(db: AsyncSession, profile_id: UUID) -> AuditorProfile:
    result = await db.execute(
        select(AuditorProfile)
        .options(selectinload(AuditorProfile.user))
        .where(AuditorProfile.id == profile_id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise NotFoundError(f"Auditor profile {profile_id} not found")
    return profile


async def get_my_profile(db: AsyncSession, user_id: UUID) -> AuditorProfile | None:
    result = await db.execute(
        select(AuditorProfile).where(AuditorProfile.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def _get_profile_by_user(db: AsyncSession, user_id: UUID) -> AuditorProfile:
    profile = await get_my_profile(db, user_id)
    if not profile:
        raise NotFoundError("No auditor profile found for this user")
    return profile


async def search_marketplace(
    db: AsyncSession,
    specialization: str | None = None,
    credential: str | None = None,
    location: str | None = None,
    verified_only: bool = False,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[dict], int]:
    """Search the public auditor marketplace."""
    base_q = (
        select(AuditorProfile, User)
        .join(User, AuditorProfile.user_id == User.id)
        .where(AuditorProfile.is_public == True)  # noqa: E712
    )
    count_q = (
        select(func.count())
        .select_from(AuditorProfile)
        .where(AuditorProfile.is_public == True)  # noqa: E712
    )

    if verified_only:
        base_q = base_q.where(AuditorProfile.is_verified == True)  # noqa: E712
        count_q = count_q.where(AuditorProfile.is_verified == True)  # noqa: E712
    if location:
        base_q = base_q.where(AuditorProfile.location.ilike(f"%{location}%"))
        count_q = count_q.where(AuditorProfile.location.ilike(f"%{location}%"))

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(
        AuditorProfile.rating.desc().nullslast()
    )
    result = await db.execute(q)
    rows = result.all()

    # Post-filter for JSON array fields (specialization/credential)
    items = []
    for profile, user in rows:
        if specialization and profile.specializations:
            if not any(
                specialization.lower() in s.lower()
                for s in profile.specializations
            ):
                continue
        if credential and profile.credentials:
            if not any(
                credential.lower() in c.lower()
                for c in profile.credentials
            ):
                continue

        items.append({
            "id": profile.id,
            "user_id": profile.user_id,
            "firm_name": profile.firm_name,
            "bio": profile.bio,
            "credentials": profile.credentials,
            "specializations": profile.specializations,
            "years_experience": profile.years_experience,
            "location": profile.location,
            "hourly_rate": profile.hourly_rate,
            "is_verified": profile.is_verified,
            "verified_at": profile.verified_at,
            "is_public": profile.is_public,
            "rating": profile.rating,
            "total_audits": profile.total_audits,
            "website_url": profile.website_url,
            "linkedin_url": profile.linkedin_url,
            "user_name": user.full_name,
            "user_email": user.email,
            "created_at": profile.created_at,
            "updated_at": profile.updated_at,
        })

    return items, total


async def verify_auditor(db: AsyncSession, profile_id: UUID) -> AuditorProfile:
    """Admin action: verify an auditor's credentials."""
    profile = await get_profile(db, profile_id)
    profile.is_verified = True
    profile.verified_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(profile)
    return profile
