"""MinIO object-storage helper with graceful degradation.

If the MinIO server is unreachable the module logs a warning on
initialisation and every subsequent call returns a sensible fallback
(empty string for URLs, ``None`` for deletes) so the rest of the
application can keep running without object storage.
"""

from __future__ import annotations

import io
import logging
from datetime import timedelta
from urllib.parse import urlparse

from minio import Minio
from minio.error import S3Error

from app.config import get_settings

logger = logging.getLogger(__name__)

_client: Minio | None = None
_available: bool = False
_ensured_buckets: set[str] = set()


def _get_client() -> Minio | None:
    """Lazily initialise the global MinIO client."""
    global _client, _available

    if _client is not None:
        return _client if _available else None

    settings = get_settings()
    parsed = urlparse(settings.MINIO_URL)
    endpoint = parsed.netloc or parsed.path  # handles "localhost:9000" or "http://…"
    secure = parsed.scheme == "https"

    try:
        _client = Minio(
            endpoint=endpoint,
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            secure=secure,
        )
        # Smoke-test connectivity by listing buckets
        _client.list_buckets()
        _available = True
        logger.info("MinIO connected at %s", endpoint)
    except Exception as exc:
        logger.warning("MinIO unavailable (%s). File storage will be disabled.", exc)
        _available = False

    return _client if _available else None


def _ensure_bucket(client: Minio, bucket: str) -> None:
    """Create the bucket if it does not already exist (cached per process)."""
    if bucket in _ensured_buckets:
        return
    try:
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
            logger.info("Created MinIO bucket: %s", bucket)
        _ensured_buckets.add(bucket)
    except S3Error as exc:
        logger.error("Failed to ensure bucket '%s': %s", bucket, exc)
        raise


def upload_file(
    bucket: str,
    object_name: str,
    data: bytes | io.BytesIO,
    content_type: str = "application/octet-stream",
) -> str:
    """Upload *data* and return the object path ``bucket/object_name``.

    Returns an empty string when MinIO is unavailable.
    """
    client = _get_client()
    if client is None:
        logger.warning("MinIO unavailable – skipping upload of %s/%s", bucket, object_name)
        return ""

    _ensure_bucket(client, bucket)

    if isinstance(data, bytes):
        data = io.BytesIO(data)

    length = data.getbuffer().nbytes if isinstance(data, io.BytesIO) else -1

    try:
        client.put_object(
            bucket_name=bucket,
            object_name=object_name,
            data=data,
            length=length,
            content_type=content_type,
        )
        logger.info("Uploaded %s/%s (%s)", bucket, object_name, content_type)
        return f"{bucket}/{object_name}"
    except S3Error as exc:
        logger.error("Upload failed for %s/%s: %s", bucket, object_name, exc)
        raise


def get_presigned_url(
    bucket: str,
    object_name: str,
    expires: timedelta | None = None,
) -> str:
    """Return a presigned GET URL valid for *expires* (default 1 hour).

    Returns an empty string when MinIO is unavailable.
    """
    client = _get_client()
    if client is None:
        logger.warning(
            "MinIO unavailable – cannot generate presigned URL for %s/%s",
            bucket,
            object_name,
        )
        return ""

    if expires is None:
        expires = timedelta(hours=1)

    try:
        url = client.presigned_get_object(
            bucket_name=bucket,
            object_name=object_name,
            expires=expires,
        )
        return url
    except S3Error as exc:
        logger.error(
            "Presigned URL generation failed for %s/%s: %s", bucket, object_name, exc
        )
        raise


def delete_file(bucket: str, object_name: str) -> None:
    """Delete an object. No-op when MinIO is unavailable."""
    client = _get_client()
    if client is None:
        logger.warning(
            "MinIO unavailable – skipping delete of %s/%s", bucket, object_name
        )
        return

    try:
        client.remove_object(bucket_name=bucket, object_name=object_name)
        logger.info("Deleted %s/%s", bucket, object_name)
    except S3Error as exc:
        logger.error("Delete failed for %s/%s: %s", bucket, object_name, exc)
        raise
