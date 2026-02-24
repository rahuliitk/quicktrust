import hashlib
from uuid import UUID

from fastapi import APIRouter, Query, UploadFile, File
from fastapi.responses import RedirectResponse

from app.core.audit_middleware import log_audit
from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.core.exceptions import BadRequestError
from app.schemas.common import PaginatedResponse
from app.schemas.evidence import EvidenceCreate, EvidenceResponse
from app.services import evidence_service

router = APIRouter(prefix="/organizations/{org_id}/evidence", tags=["evidence"])


@router.get("", response_model=PaginatedResponse)
async def list_evidence(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    control_id: UUID | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await evidence_service.list_evidence(
        db, org_id, control_id=control_id, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[EvidenceResponse.model_validate(e) for e in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=EvidenceResponse, status_code=201)
async def create_evidence(org_id: VerifiedOrgId, data: EvidenceCreate, db: DB, current_user: ComplianceUser):
    item = await evidence_service.create_evidence(db, org_id, data)
    await log_audit(db, current_user, "create", "evidence", str(item.id), org_id)
    return item


@router.get("/{evidence_id}", response_model=EvidenceResponse)
async def get_evidence(org_id: VerifiedOrgId, evidence_id: UUID, db: DB, current_user: AnyInternalUser):
    return await evidence_service.get_evidence(db, org_id, evidence_id)


@router.post("/{evidence_id}/upload", response_model=EvidenceResponse)
async def upload_evidence_file(
    org_id: VerifiedOrgId,
    evidence_id: UUID,
    db: DB,
    current_user: ComplianceUser,
    file: UploadFile = File(...),
):
    """Upload an evidence file to object storage and associate it with the evidence record."""
    from app.core.storage import upload_file

    evidence = await evidence_service.get_evidence(db, org_id, evidence_id)

    contents = await file.read()

    # Compute SHA-256 hash of the uploaded file for integrity tracking
    file_hash = hashlib.sha256(contents).hexdigest()

    # Determine content type
    content_type = file.content_type or "application/octet-stream"
    original_name = file.filename or "upload"

    object_name = f"evidence/{org_id}/{evidence_id}/{original_name}"
    file_url = upload_file(
        bucket="quicktrust-evidence",
        object_name=object_name,
        data=contents,
        content_type=content_type,
    )

    if not file_url:
        raise BadRequestError("File storage is currently unavailable. Upload failed.")

    evidence.file_url = file_url
    evidence.file_name = original_name
    evidence.artifact_hash = file_hash
    await db.commit()
    await db.refresh(evidence)

    await log_audit(db, current_user, "upload_file", "evidence", str(evidence_id), org_id)
    return evidence


@router.get("/{evidence_id}/download")
async def download_evidence_file(
    org_id: VerifiedOrgId, evidence_id: UUID, db: DB, current_user: AnyInternalUser
):
    """Download an evidence file via presigned URL redirect."""
    from app.core.storage import get_presigned_url

    evidence = await evidence_service.get_evidence(db, org_id, evidence_id)

    if not evidence.file_url:
        raise BadRequestError("No file has been uploaded for this evidence item.")

    # file_url is stored as "bucket/object_name"
    parts = evidence.file_url.split("/", 1)
    if len(parts) != 2:
        raise BadRequestError("Invalid file reference on this evidence item.")

    bucket, object_name = parts
    presigned_url = get_presigned_url(bucket=bucket, object_name=object_name)

    if not presigned_url:
        raise BadRequestError("File storage is currently unavailable.")

    return RedirectResponse(url=presigned_url, status_code=307)
