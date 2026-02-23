from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.collection_job import CollectionJob
from app.models.evidence import Evidence
from app.models.integration import Integration
from app.collectors.base import COLLECTOR_REGISTRY
from app.schemas.integration import CollectionTrigger


async def trigger_collection(
    db: AsyncSession, org_id: UUID, integration_id: UUID, data: CollectionTrigger
) -> CollectionJob:
    """Create a collection job, run the collector, and create an Evidence record."""
    # Verify integration exists
    result = await db.execute(
        select(Integration).where(
            Integration.id == integration_id, Integration.org_id == org_id
        )
    )
    integration = result.scalar_one_or_none()
    if not integration:
        raise NotFoundError(f"Integration {integration_id} not found")

    # Create collection job
    job = CollectionJob(
        org_id=org_id,
        integration_id=integration_id,
        evidence_template_id=data.evidence_template_id,
        control_id=data.control_id,
        collector_type=data.collector_type,
        status="running",
    )
    db.add(job)
    await db.flush()

    # Run collector
    collector = COLLECTOR_REGISTRY.get(data.collector_type)
    if not collector:
        job.status = "failed"
        job.error_message = f"Unknown collector type: {data.collector_type}"
        await db.commit()
        await db.refresh(job)
        return job

    try:
        result_data = await collector.collect(
            config=integration.config or {},
            credentials=None,
        )
        job.result_data = result_data
        job.status = "completed"

        # Create evidence record
        evidence = Evidence(
            org_id=org_id,
            control_id=data.control_id,
            template_id=data.evidence_template_id,
            title=f"Auto-collected: {result_data.get('summary', data.collector_type)}",
            status="collected",
            collected_at=datetime.now(timezone.utc),
            data=result_data.get("data", {}),
            collection_method="automated",
            collector=data.collector_type,
        )
        db.add(evidence)
        await db.flush()
        job.evidence_id = evidence.id

        # Update integration last_sync
        integration.last_sync_at = datetime.now(timezone.utc)

    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)

    await db.commit()
    await db.refresh(job)
    return job


async def list_collection_jobs(
    db: AsyncSession, org_id: UUID, integration_id: UUID,
    page: int = 1, page_size: int = 50,
) -> tuple[list[CollectionJob], int]:
    base_q = select(CollectionJob).where(
        CollectionJob.org_id == org_id,
        CollectionJob.integration_id == integration_id,
    )
    count_q = select(func.count()).select_from(CollectionJob).where(
        CollectionJob.org_id == org_id,
        CollectionJob.integration_id == integration_id,
    )
    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(CollectionJob.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total
