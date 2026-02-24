from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.trust_center import TrustCenterConfig, TrustCenterDocument
from app.schemas.trust_center import (
    TrustCenterConfigCreate, TrustCenterConfigUpdate,
    TrustCenterDocumentCreate, TrustCenterDocumentUpdate,
)


# === Config ===

async def get_or_create_config(db: AsyncSession, org_id: UUID, data: TrustCenterConfigCreate | None = None) -> TrustCenterConfig:
    result = await db.execute(
        select(TrustCenterConfig).where(TrustCenterConfig.org_id == org_id)
    )
    config = result.scalar_one_or_none()
    if config:
        return config

    if data is None:
        from app.models.organization import Organization
        org_result = await db.execute(select(Organization).where(Organization.id == org_id))
        org = org_result.scalar_one_or_none()
        slug = org.slug if org else str(org_id)[:8]
        config = TrustCenterConfig(org_id=org_id, slug=slug)
    else:
        config = TrustCenterConfig(org_id=org_id, **data.model_dump())

    db.add(config)
    await db.commit()
    await db.refresh(config)
    return config


async def get_config(db: AsyncSession, org_id: UUID) -> TrustCenterConfig:
    result = await db.execute(
        select(TrustCenterConfig).where(TrustCenterConfig.org_id == org_id)
    )
    config = result.scalar_one_or_none()
    if not config:
        raise NotFoundError("Trust center config not found")
    return config


async def update_config(
    db: AsyncSession, org_id: UUID, data: TrustCenterConfigUpdate
) -> TrustCenterConfig:
    config = await get_config(db, org_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(config, field, value)
    await db.commit()
    await db.refresh(config)
    return config


# === Documents ===

async def list_documents(db: AsyncSession, org_id: UUID) -> list[TrustCenterDocument]:
    result = await db.execute(
        select(TrustCenterDocument)
        .where(TrustCenterDocument.org_id == org_id)
        .order_by(TrustCenterDocument.sort_order)
    )
    return list(result.scalars().all())


async def create_document(db: AsyncSession, org_id: UUID, data: TrustCenterDocumentCreate) -> TrustCenterDocument:
    doc = TrustCenterDocument(org_id=org_id, **data.model_dump())
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc


async def get_document(db: AsyncSession, org_id: UUID, doc_id: UUID) -> TrustCenterDocument:
    result = await db.execute(
        select(TrustCenterDocument).where(
            TrustCenterDocument.id == doc_id, TrustCenterDocument.org_id == org_id
        )
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise NotFoundError(f"Document {doc_id} not found")
    return doc


async def update_document(
    db: AsyncSession, org_id: UUID, doc_id: UUID, data: TrustCenterDocumentUpdate
) -> TrustCenterDocument:
    doc = await get_document(db, org_id, doc_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(doc, field, value)
    await db.commit()
    await db.refresh(doc)
    return doc


async def delete_document(db: AsyncSession, org_id: UUID, doc_id: UUID) -> None:
    doc = await get_document(db, org_id, doc_id)
    await db.delete(doc)
    await db.commit()


# === Public ===

async def get_public_trust_center(db: AsyncSession, slug: str) -> dict | None:
    result = await db.execute(
        select(TrustCenterConfig).where(
            TrustCenterConfig.slug == slug,
            TrustCenterConfig.is_published == True,
        )
    )
    config = result.scalar_one_or_none()
    if not config:
        return None

    docs_result = await db.execute(
        select(TrustCenterDocument).where(
            TrustCenterDocument.org_id == config.org_id,
            TrustCenterDocument.is_public == True,
        ).order_by(TrustCenterDocument.sort_order)
    )
    documents = list(docs_result.scalars().all())

    return {
        "slug": config.slug,
        "headline": config.headline,
        "description": config.description,
        "contact_email": config.contact_email,
        "logo_url": config.logo_url,
        "certifications": config.certifications,
        "branding": config.branding,
        "documents": documents,
    }
