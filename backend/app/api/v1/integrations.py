from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, CurrentUser
from app.schemas.common import PaginatedResponse
from app.schemas.integration import (
    IntegrationCreate,
    IntegrationUpdate,
    IntegrationResponse,
    CollectionTrigger,
    CollectionJobResponse,
    ProviderInfo,
)
from app.services import integration_service, collection_service

router = APIRouter(
    prefix="/organizations/{org_id}/integrations",
    tags=["integrations"],
)

PROVIDERS = [
    ProviderInfo(
        provider="aws",
        name="Amazon Web Services",
        description="Collect IAM, CloudTrail, encryption, and infrastructure evidence from AWS.",
        collector_types=["aws_iam_mfa_report", "aws_cloudtrail_status", "aws_encryption_at_rest"],
    ),
    ProviderInfo(
        provider="github",
        name="GitHub",
        description="Collect branch protection, Dependabot alerts, and code review evidence.",
        collector_types=["github_branch_protection", "github_dependabot_alerts"],
    ),
    ProviderInfo(
        provider="okta",
        name="Okta",
        description="Collect MFA enrollment and identity management evidence.",
        collector_types=["okta_mfa_enrollment"],
    ),
]


@router.get("/providers", response_model=list[ProviderInfo])
async def list_providers(org_id: UUID, db: DB, current_user: CurrentUser):
    return PROVIDERS


@router.get("", response_model=PaginatedResponse)
async def list_integrations(
    org_id: UUID, db: DB, current_user: CurrentUser,
    page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100),
):
    items, total = await integration_service.list_integrations(db, org_id, page, page_size)
    return PaginatedResponse(
        items=[IntegrationResponse.model_validate(i) for i in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=IntegrationResponse, status_code=201)
async def create_integration(
    org_id: UUID, data: IntegrationCreate, db: DB, current_user: CurrentUser
):
    return await integration_service.create_integration(db, org_id, data)


@router.get("/{integration_id}", response_model=IntegrationResponse)
async def get_integration(
    org_id: UUID, integration_id: UUID, db: DB, current_user: CurrentUser
):
    return await integration_service.get_integration(db, org_id, integration_id)


@router.patch("/{integration_id}", response_model=IntegrationResponse)
async def update_integration(
    org_id: UUID, integration_id: UUID, data: IntegrationUpdate,
    db: DB, current_user: CurrentUser,
):
    return await integration_service.update_integration(db, org_id, integration_id, data)


@router.delete("/{integration_id}", status_code=204)
async def delete_integration(
    org_id: UUID, integration_id: UUID, db: DB, current_user: CurrentUser
):
    await integration_service.delete_integration(db, org_id, integration_id)


@router.post("/{integration_id}/test")
async def test_integration(
    org_id: UUID, integration_id: UUID, db: DB, current_user: CurrentUser
):
    integration = await integration_service.get_integration(db, org_id, integration_id)
    return {"status": "ok", "provider": integration.provider, "message": "Connection test successful"}


@router.post("/{integration_id}/collect", response_model=CollectionJobResponse)
async def trigger_collection(
    org_id: UUID, integration_id: UUID, data: CollectionTrigger,
    db: DB, current_user: CurrentUser,
):
    return await collection_service.trigger_collection(db, org_id, integration_id, data)


@router.get("/{integration_id}/jobs", response_model=PaginatedResponse)
async def list_collection_jobs(
    org_id: UUID, integration_id: UUID, db: DB, current_user: CurrentUser,
    page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100),
):
    items, total = await collection_service.list_collection_jobs(
        db, org_id, integration_id, page, page_size
    )
    return PaginatedResponse(
        items=[CollectionJobResponse.model_validate(i) for i in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )
