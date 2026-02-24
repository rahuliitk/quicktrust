from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.report import Report
from app.schemas.report import ReportCreate


async def list_reports(
    db: AsyncSession,
    org_id: UUID,
    report_type: str | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[Report], int]:
    base_q = select(Report).where(Report.org_id == org_id)
    count_q = select(func.count()).select_from(Report).where(Report.org_id == org_id)

    if report_type:
        base_q = base_q.where(Report.report_type == report_type)
        count_q = count_q.where(Report.report_type == report_type)
    if status:
        base_q = base_q.where(Report.status == status)
        count_q = count_q.where(Report.status == status)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(Report.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_report(
    db: AsyncSession, org_id: UUID, data: ReportCreate, requested_by_id: UUID | None = None
) -> Report:
    report = Report(
        org_id=org_id,
        requested_by_id=requested_by_id,
        **data.model_dump(),
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


async def get_report(db: AsyncSession, org_id: UUID, report_id: UUID) -> Report:
    result = await db.execute(
        select(Report).where(Report.id == report_id, Report.org_id == org_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise NotFoundError(f"Report {report_id} not found")
    return report


async def delete_report(db: AsyncSession, org_id: UUID, report_id: UUID) -> None:
    report = await get_report(db, org_id, report_id)
    await db.delete(report)
    await db.commit()


async def generate_report_data(db: AsyncSession, org_id: UUID, report_id: UUID) -> dict:
    """Generate report data by aggregating from existing services."""
    report = await get_report(db, org_id, report_id)
    report.status = "generating"
    await db.commit()

    try:
        from app.services import control_service, risk_service
        from app.models.policy import Policy
        from app.models.evidence import Evidence
        from app.models.training import TrainingAssignment

        data: dict = {"report_type": report.report_type, "generated_at": datetime.now(timezone.utc).isoformat()}

        if report.report_type in ("compliance_summary", "evidence_audit"):
            control_stats = await control_service.get_control_stats(db, org_id)
            data["control_stats"] = {
                "total": control_stats.total,
                "draft": control_stats.draft,
                "implemented": control_stats.implemented,
            }

        if report.report_type in ("compliance_summary", "risk_report"):
            risk_stats = await risk_service.get_risk_stats(db, org_id)
            data["risk_stats"] = risk_stats

        if report.report_type in ("compliance_summary",):
            policy_count = (await db.execute(
                select(func.count()).select_from(Policy).where(Policy.org_id == org_id)
            )).scalar() or 0
            published_count = (await db.execute(
                select(func.count()).select_from(Policy).where(
                    Policy.org_id == org_id, Policy.status == "published"
                )
            )).scalar() or 0
            data["policy_stats"] = {"total": policy_count, "published": published_count}

        if report.report_type in ("compliance_summary", "evidence_audit"):
            evidence_count = (await db.execute(
                select(func.count()).select_from(Evidence).where(Evidence.org_id == org_id)
            )).scalar() or 0
            data["evidence_stats"] = {"total": evidence_count}

        if report.report_type == "training_completion":
            total_assignments = (await db.execute(
                select(func.count()).select_from(TrainingAssignment).where(TrainingAssignment.org_id == org_id)
            )).scalar() or 0
            completed = (await db.execute(
                select(func.count()).select_from(TrainingAssignment).where(
                    TrainingAssignment.org_id == org_id, TrainingAssignment.status == "completed"
                )
            )).scalar() or 0
            data["training_stats"] = {
                "total_assignments": total_assignments,
                "completed": completed,
                "completion_rate": round((completed / total_assignments * 100), 1) if total_assignments else 0.0,
            }

        # Render to the requested format and upload to MinIO
        if report.format in ("pdf", "csv"):
            from app.services.report_renderer import render_pdf, render_csv
            from app.core.storage import upload_file

            if report.format == "pdf":
                file_bytes = render_pdf(data, report.report_type)
                content_type = "application/pdf"
                extension = "pdf"
            else:
                file_bytes = render_csv(data, report.report_type)
                content_type = "text/csv"
                extension = "csv"

            object_name = (
                f"reports/{org_id}/{report_id}.{extension}"
            )
            file_url = upload_file(
                bucket="quicktrust-reports",
                object_name=object_name,
                data=file_bytes,
                content_type=content_type,
            )
            report.file_url = file_url if file_url else None

        report.status = "completed"
        report.generated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(report)
        return data

    except Exception as e:
        report.status = "failed"
        report.error_message = str(e)
        await db.commit()
        return {"error": str(e)}


async def get_report_stats(db: AsyncSession, org_id: UUID) -> dict:
    result = await db.execute(select(Report).where(Report.org_id == org_id))
    reports = list(result.scalars().all())

    by_type: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for r in reports:
        by_type[r.report_type] = by_type.get(r.report_type, 0) + 1
        by_status[r.status] = by_status.get(r.status, 0) + 1

    return {
        "total": len(reports),
        "by_type": by_type,
        "by_status": by_status,
    }
