from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser
from app.schemas.common import PaginatedResponse
from app.schemas.access_review import (
    AccessReviewCampaignCreate,
    AccessReviewCampaignUpdate,
    AccessReviewCampaignResponse,
    AccessReviewEntryCreate,
    AccessReviewEntryUpdate,
    AccessReviewEntryResponse,
    AccessReviewStatsResponse,
)
from app.services import access_review_service

router = APIRouter(
    prefix="/organizations/{org_id}/access-reviews",
    tags=["access-reviews"],
)


@router.get("", response_model=PaginatedResponse)
async def list_campaigns(
    org_id: UUID,
    db: DB,
    current_user: AnyInternalUser,
    status: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await access_review_service.list_campaigns(
        db, org_id, status=status, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[AccessReviewCampaignResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=AccessReviewCampaignResponse, status_code=201)
async def create_campaign(org_id: UUID, data: AccessReviewCampaignCreate, db: DB, current_user: ComplianceUser):
    campaign = await access_review_service.create_campaign(db, org_id, data)
    return AccessReviewCampaignResponse.model_validate({
        **{col: getattr(campaign, col) for col in campaign.__table__.columns.keys()},
        "entry_count": 0,
        "pending_count": 0,
    })


@router.get("/stats", response_model=AccessReviewStatsResponse)
async def get_stats(org_id: UUID, db: DB, current_user: AnyInternalUser):
    return await access_review_service.get_access_review_stats(db, org_id)


@router.get("/{campaign_id}", response_model=AccessReviewCampaignResponse)
async def get_campaign(org_id: UUID, campaign_id: UUID, db: DB, current_user: AnyInternalUser):
    return await access_review_service.get_campaign_response(db, org_id, campaign_id)


@router.patch("/{campaign_id}", response_model=AccessReviewCampaignResponse)
async def update_campaign(
    org_id: UUID, campaign_id: UUID, data: AccessReviewCampaignUpdate, db: DB, current_user: ComplianceUser
):
    campaign = await access_review_service.update_campaign(db, org_id, campaign_id, data)
    return await access_review_service.get_campaign_response(db, org_id, campaign_id)


@router.delete("/{campaign_id}", status_code=204)
async def delete_campaign(org_id: UUID, campaign_id: UUID, db: DB, current_user: ComplianceUser):
    await access_review_service.delete_campaign(db, org_id, campaign_id)


# === Entries ===

@router.get("/{campaign_id}/entries", response_model=list[AccessReviewEntryResponse])
async def list_entries(
    org_id: UUID, campaign_id: UUID, db: DB, current_user: AnyInternalUser,
    decision: str | None = None,
):
    return await access_review_service.list_entries(db, org_id, campaign_id, decision=decision)


@router.post("/{campaign_id}/entries", response_model=AccessReviewEntryResponse, status_code=201)
async def create_entry(
    org_id: UUID, campaign_id: UUID, data: AccessReviewEntryCreate, db: DB, current_user: ComplianceUser
):
    return await access_review_service.create_entry(db, org_id, campaign_id, data)


@router.patch("/{campaign_id}/entries/{entry_id}", response_model=AccessReviewEntryResponse)
async def update_entry(
    org_id: UUID, campaign_id: UUID, entry_id: UUID,
    data: AccessReviewEntryUpdate, db: DB, current_user: CurrentUser,
):
    return await access_review_service.update_entry(
        db, org_id, campaign_id, entry_id, data, decided_by_id=current_user.id
    )
