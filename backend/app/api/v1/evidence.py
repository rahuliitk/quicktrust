from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, CurrentUser
from app.schemas.common import PaginatedResponse
from app.schemas.evidence import EvidenceCreate, EvidenceResponse
from app.services import evidence_service

router = APIRouter(prefix="/organizations/{org_id}/evidence", tags=["evidence"])


@router.get("", response_model=PaginatedResponse)
async def list_evidence(
    org_id: UUID,
    db: DB,
    current_user: CurrentUser,
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
async def create_evidence(org_id: UUID, data: EvidenceCreate, db: DB, current_user: CurrentUser):
    return await evidence_service.create_evidence(db, org_id, data)


@router.get("/{evidence_id}", response_model=EvidenceResponse)
async def get_evidence(org_id: UUID, evidence_id: UUID, db: DB, current_user: CurrentUser):
    return await evidence_service.get_evidence(db, org_id, evidence_id)
