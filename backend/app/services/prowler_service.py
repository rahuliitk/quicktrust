"""Business logic for Prowler security scanner operations."""
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.collection_job import CollectionJob
from app.models.integration import Integration
from app.schemas.integration import CollectionTrigger
from app.schemas.prowler import (
    ProwlerScanTrigger,
    ProwlerFinding,
    ProwlerScanResultResponse,
    ProwlerCompliancePosture,
    ProwlerFindingSummary,
    ComplianceFrameworkPosture,
    ServicePosture,
)
from app.services import collection_service


SCAN_TYPE_TO_COLLECTOR = {
    "full": "prowler_aws_full_scan",
    "service": "prowler_aws_service_scan",
    "compliance": "prowler_aws_compliance_scan",
}


async def trigger_scan(
    db: AsyncSession, org_id: UUID, data: ProwlerScanTrigger
) -> CollectionJob:
    """Trigger a Prowler scan via the collection service."""
    collector_type = SCAN_TYPE_TO_COLLECTOR.get(data.scan_type, "prowler_aws_full_scan")

    # Build config for the collector
    integration_id = UUID(data.integration_id)

    # Update integration config with scan parameters
    result = await db.execute(
        select(Integration).where(
            Integration.id == integration_id, Integration.org_id == org_id
        )
    )
    integration = result.scalar_one_or_none()
    if integration:
        config = dict(integration.config or {})
        if data.services:
            config["services"] = data.services
        if data.compliance_framework:
            config["compliance_framework"] = data.compliance_framework
        integration.config = config
        await db.flush()

    trigger = CollectionTrigger(collector_type=collector_type)
    return await collection_service.trigger_collection(db, org_id, integration_id, trigger)


async def list_scan_results(
    db: AsyncSession,
    org_id: UUID,
    severity: str | None = None,
    status: str | None = None,
    service: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[ProwlerScanResultResponse], int]:
    """List Prowler scan results (collection jobs with prowler_ collector types)."""
    base_q = select(CollectionJob).where(
        CollectionJob.org_id == org_id,
        CollectionJob.collector_type.like("prowler_%"),
    )
    count_q = select(func.count()).select_from(CollectionJob).where(
        CollectionJob.org_id == org_id,
        CollectionJob.collector_type.like("prowler_%"),
    )

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(
        CollectionJob.created_at.desc()
    )
    result = await db.execute(q)
    jobs = list(result.scalars().all())

    responses = []
    for job in jobs:
        data = job.result_data or {}
        inner = data.get("data", {})
        stats = inner.get("summary_stats", {})

        # Apply filters at the response level
        findings_list = inner.get("findings", [])
        if severity:
            findings_list = [f for f in findings_list if f.get("severity", "").lower() == severity.lower()]
        if status:
            findings_list = [f for f in findings_list if f.get("status", "").upper() == status.upper()]
        if service:
            findings_list = [f for f in findings_list if f.get("service", "").lower() == service.lower()]

        responses.append(ProwlerScanResultResponse(
            job_id=str(job.id),
            status=job.status,
            scan_type=inner.get("scan_type"),
            cloud_provider=inner.get("cloud_provider"),
            total_findings=stats.get("total", 0),
            passed=stats.get("passed", 0),
            failed=stats.get("failed", 0),
            pass_rate=stats.get("pass_rate", 0.0),
            created_at=job.created_at.isoformat() if job.created_at else None,
            findings=[ProwlerFinding(**f) for f in findings_list],
        ))

    return responses, total


async def get_scan_detail(
    db: AsyncSession, org_id: UUID, job_id: UUID
) -> ProwlerScanResultResponse | None:
    """Get detailed results for a specific Prowler scan job."""
    result = await db.execute(
        select(CollectionJob).where(
            CollectionJob.id == job_id,
            CollectionJob.org_id == org_id,
            CollectionJob.collector_type.like("prowler_%"),
        )
    )
    job = result.scalar_one_or_none()
    if not job:
        return None

    data = job.result_data or {}
    inner = data.get("data", {})
    stats = inner.get("summary_stats", {})
    findings_list = inner.get("findings", [])

    return ProwlerScanResultResponse(
        job_id=str(job.id),
        status=job.status,
        scan_type=inner.get("scan_type"),
        cloud_provider=inner.get("cloud_provider"),
        total_findings=stats.get("total", 0),
        passed=stats.get("passed", 0),
        failed=stats.get("failed", 0),
        pass_rate=stats.get("pass_rate", 0.0),
        created_at=job.created_at.isoformat() if job.created_at else None,
        findings=[ProwlerFinding(**f) for f in findings_list],
    )


async def get_compliance_posture(
    db: AsyncSession, org_id: UUID
) -> ProwlerCompliancePosture:
    """Aggregate compliance posture from all completed Prowler scans."""
    result = await db.execute(
        select(CollectionJob)
        .where(
            CollectionJob.org_id == org_id,
            CollectionJob.collector_type.like("prowler_%"),
            CollectionJob.status == "completed",
        )
        .order_by(CollectionJob.created_at.desc())
        .limit(20)
    )
    jobs = list(result.scalars().all())

    if not jobs:
        return ProwlerCompliancePosture()

    # Aggregate from the latest scan
    latest = jobs[0]
    data = (latest.result_data or {}).get("data", {})
    findings = data.get("findings", [])

    # Build framework posture from compliance field in findings
    framework_map: dict[str, dict] = {}
    service_map: dict[str, dict] = {}

    for f in findings:
        svc = f.get("service", "Unknown")
        is_pass = f.get("status", "").upper() == "PASS"

        if svc not in service_map:
            service_map[svc] = {"total": 0, "passed": 0, "failed": 0}
        service_map[svc]["total"] += 1
        if is_pass:
            service_map[svc]["passed"] += 1
        else:
            service_map[svc]["failed"] += 1

        compliance = f.get("compliance", {})
        for fw, _ in compliance.items():
            if fw not in framework_map:
                framework_map[fw] = {"total": 0, "passed": 0, "failed": 0}
            framework_map[fw]["total"] += 1
            if is_pass:
                framework_map[fw]["passed"] += 1
            else:
                framework_map[fw]["failed"] += 1

    frameworks = [
        ComplianceFrameworkPosture(
            framework=fw,
            total_checks=v["total"],
            passed=v["passed"],
            failed=v["failed"],
            pass_rate=round(v["passed"] / v["total"] * 100, 1) if v["total"] > 0 else 0.0,
        )
        for fw, v in framework_map.items()
    ]

    services = [
        ServicePosture(
            service=svc,
            total_checks=v["total"],
            passed=v["passed"],
            failed=v["failed"],
            pass_rate=round(v["passed"] / v["total"] * 100, 1) if v["total"] > 0 else 0.0,
        )
        for svc, v in service_map.items()
    ]

    total_checks = sum(1 for _ in findings)
    total_passed = sum(1 for f in findings if f.get("status", "").upper() == "PASS")
    overall = round(total_passed / total_checks * 100, 1) if total_checks > 0 else 0.0

    return ProwlerCompliancePosture(
        frameworks=frameworks,
        services=services,
        overall_pass_rate=overall,
        total_scans=len(jobs),
        last_scan_at=latest.created_at.isoformat() if latest.created_at else None,
    )


async def get_findings_summary(
    db: AsyncSession, org_id: UUID
) -> ProwlerFindingSummary:
    """Summary stats from the most recent completed Prowler scan."""
    result = await db.execute(
        select(CollectionJob)
        .where(
            CollectionJob.org_id == org_id,
            CollectionJob.collector_type.like("prowler_%"),
            CollectionJob.status == "completed",
        )
        .order_by(CollectionJob.created_at.desc())
        .limit(1)
    )
    job = result.scalar_one_or_none()

    if not job:
        return ProwlerFindingSummary()

    data = (job.result_data or {}).get("data", {})
    stats = data.get("summary_stats", {})

    by_severity = stats.get("by_severity", {})

    return ProwlerFindingSummary(
        total=stats.get("total", 0),
        passed=stats.get("passed", 0),
        failed=stats.get("failed", 0),
        pass_rate=stats.get("pass_rate", 0.0),
        by_severity=by_severity,
        by_service=stats.get("by_service", {}),
        critical_count=by_severity.get("critical", 0),
        high_count=by_severity.get("high", 0),
        last_scan_at=job.created_at.isoformat() if job.created_at else None,
    )
