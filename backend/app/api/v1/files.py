"""File upload / download endpoints.

Follows the same pattern as controls.py and evidence.py:
- Router prefix scoped under an organization
- Uses ``DB`` and ``CurrentUser`` dependency aliases
- Multipart file upload via ``python-multipart``
"""

from __future__ import annotations

import uuid as _uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile, File, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy import select

from app.config import get_settings
from app.core.dependencies import DB, CurrentUser
from app.core.storage import upload_file, get_presigned_url, delete_file

router = APIRouter(
    prefix="/organizations/{org_id}/files",
    tags=["files"],
)


# ---------------------------------------------------------------------------
# Response schemas (co-located because they are small & endpoint-specific)
# ---------------------------------------------------------------------------

class FileUploadResponse(BaseModel):
    id: str
    filename: str
    content_type: str
    size: int
    object_path: str
    uploaded_at: str


class FileDeleteResponse(BaseModel):
    message: str


# ---------------------------------------------------------------------------
# Allowed file types & size limits
# ---------------------------------------------------------------------------
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

ALLOWED_CONTENT_TYPES = {
    # Documents
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    # Text
    "text/plain",
    "text/csv",
    "text/markdown",
    # Images
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/webp",
    "image/svg+xml",
    # Archives
    "application/zip",
    "application/gzip",
    # JSON / YAML
    "application/json",
    "application/x-yaml",
    "text/yaml",
}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/upload", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload(
    org_id: _uuid.UUID,
    db: DB,
    current_user: CurrentUser,
    file: UploadFile = File(...),
):
    """Upload a file to object storage.

    The file is stored under
    ``<bucket>/<org_id>/<YYYY-MM-DD>/<file_id>_<original_name>``.
    """
    # --- Validation ---------------------------------------------------------
    if file.content_type and file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Content type '{file.content_type}' is not allowed.",
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds the {MAX_FILE_SIZE // (1024 * 1024)} MB limit.",
        )

    # --- Build object path --------------------------------------------------
    settings = get_settings()
    bucket = settings.MINIO_BUCKET
    file_id = str(_uuid.uuid4())
    today = datetime.utcnow().strftime("%Y-%m-%d")
    safe_filename = (file.filename or "upload").replace("/", "_").replace("\\", "_")
    object_name = f"{org_id}/{today}/{file_id}_{safe_filename}"

    content_type = file.content_type or "application/octet-stream"

    # --- Upload -------------------------------------------------------------
    object_path = upload_file(
        bucket=bucket,
        object_name=object_name,
        data=contents,
        content_type=content_type,
    )

    if not object_path:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="File storage service is currently unavailable. Please try again later.",
        )

    return FileUploadResponse(
        id=file_id,
        filename=safe_filename,
        content_type=content_type,
        size=len(contents),
        object_path=object_path,
        uploaded_at=datetime.utcnow().isoformat(),
    )


@router.get("/{file_id}/download")
async def download(
    org_id: _uuid.UUID,
    file_id: str,
    db: DB,
    current_user: CurrentUser,
    object_path: str | None = None,
):
    """Redirect the caller to a time-limited presigned download URL.

    The client must supply the ``object_path`` query parameter that was
    returned from the upload endpoint (e.g.
    ``quicktrust-evidence/org-id/2024-01-01/file-id_name.pdf``).

    In a production system this would look up the file record from the DB;
    for now we accept the path as a query parameter for simplicity.
    """
    if not object_path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'object_path' query parameter is required.",
        )

    # object_path format: "bucket/rest/of/key"
    parts = object_path.split("/", 1)
    if len(parts) != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid object_path format. Expected 'bucket/object_name'.",
        )

    bucket, object_name = parts

    # Ensure the object belongs to the requesting organization
    if not object_name.startswith(str(org_id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: file does not belong to this organization.",
        )

    url = get_presigned_url(bucket=bucket, object_name=object_name)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="File storage service is currently unavailable.",
        )

    return RedirectResponse(url=url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@router.delete("/{file_id}", response_model=FileDeleteResponse)
async def delete(
    org_id: _uuid.UUID,
    file_id: str,
    db: DB,
    current_user: CurrentUser,
    object_path: str | None = None,
):
    """Delete a file from object storage."""
    if not object_path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'object_path' query parameter is required.",
        )

    parts = object_path.split("/", 1)
    if len(parts) != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid object_path format. Expected 'bucket/object_name'.",
        )

    bucket, object_name = parts

    if not object_name.startswith(str(org_id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: file does not belong to this organization.",
        )

    delete_file(bucket=bucket, object_name=object_name)

    return FileDeleteResponse(message=f"File {file_id} deleted successfully.")
