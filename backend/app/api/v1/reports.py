from uuid import UUID

from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser
from app.core.exceptions import BadRequestError
from app.schemas.common import PaginatedResponse
from app.schemas.report import ReportCreate, ReportResponse, ReportStatsResponse
from app.services import report_service

router = APIRouter(
    prefix="/organizations/{org_id}/reports",
    tags=["reports"],
)


@router.get("", response_model=PaginatedResponse)
async def list_reports(
    org_id: UUID,
    db: DB,
    current_user: AnyInternalUser,
    report_type: str | None = None,
    status: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await report_service.list_reports(
        db, org_id, report_type=report_type, status=status, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[ReportResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=ReportResponse, status_code=201)
async def create_report(org_id: UUID, data: ReportCreate, db: DB, current_user: ComplianceUser):
    return await report_service.create_report(db, org_id, data, requested_by_id=current_user.id)


@router.get("/stats", response_model=ReportStatsResponse)
async def get_stats(org_id: UUID, db: DB, current_user: AnyInternalUser):
    return await report_service.get_report_stats(db, org_id)


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(org_id: UUID, report_id: UUID, db: DB, current_user: AnyInternalUser):
    return await report_service.get_report(db, org_id, report_id)


@router.delete("/{report_id}", status_code=204)
async def delete_report(org_id: UUID, report_id: UUID, db: DB, current_user: ComplianceUser):
    await report_service.delete_report(db, org_id, report_id)


@router.get("/{report_id}/download")
async def download_report(org_id: UUID, report_id: UUID, db: DB, current_user: AnyInternalUser):
    """Download a rendered report file (PDF/CSV) via presigned URL redirect."""
    from app.core.storage import get_presigned_url

    report = await report_service.get_report(db, org_id, report_id)

    if not report.file_url:
        raise BadRequestError(
            "No file available for this report. "
            "Generate the report in PDF or CSV format first."
        )

    # file_url is stored as "bucket/object_name"
    parts = report.file_url.split("/", 1)
    if len(parts) != 2:
        raise BadRequestError("Invalid file reference on this report.")

    bucket, object_name = parts
    presigned_url = get_presigned_url(bucket=bucket, object_name=object_name)

    if not presigned_url:
        raise BadRequestError("File storage is currently unavailable.")

    return RedirectResponse(url=presigned_url, status_code=307)


@router.get("/{report_id}/data")
async def get_report_data(org_id: UUID, report_id: UUID, db: DB, current_user: AnyInternalUser):
    return await report_service.generate_report_data(db, org_id, report_id)
