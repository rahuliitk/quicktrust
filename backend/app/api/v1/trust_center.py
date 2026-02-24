from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.schemas.trust_center import (
    TrustCenterConfigCreate,
    TrustCenterConfigUpdate,
    TrustCenterConfigResponse,
    TrustCenterDocumentCreate,
    TrustCenterDocumentUpdate,
    TrustCenterDocumentResponse,
    PublicTrustCenterResponse,
)
from app.services import trust_center_service
from app.core.exceptions import NotFoundError

# Authenticated routes
router = APIRouter(
    prefix="/organizations/{org_id}/trust-center",
    tags=["trust-center"],
)


@router.get("/config", response_model=TrustCenterConfigResponse)
async def get_config(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    return await trust_center_service.get_or_create_config(db, org_id)


@router.post("/config", response_model=TrustCenterConfigResponse, status_code=201)
async def create_config(org_id: VerifiedOrgId, data: TrustCenterConfigCreate, db: DB, current_user: ComplianceUser):
    return await trust_center_service.get_or_create_config(db, org_id, data)


@router.patch("/config", response_model=TrustCenterConfigResponse)
async def update_config(org_id: VerifiedOrgId, data: TrustCenterConfigUpdate, db: DB, current_user: ComplianceUser):
    return await trust_center_service.update_config(db, org_id, data)


@router.get("/documents", response_model=list[TrustCenterDocumentResponse])
async def list_documents(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    return await trust_center_service.list_documents(db, org_id)


@router.post("/documents", response_model=TrustCenterDocumentResponse, status_code=201)
async def create_document(org_id: VerifiedOrgId, data: TrustCenterDocumentCreate, db: DB, current_user: ComplianceUser):
    return await trust_center_service.create_document(db, org_id, data)


@router.get("/documents/{doc_id}", response_model=TrustCenterDocumentResponse)
async def get_document(org_id: VerifiedOrgId, doc_id: UUID, db: DB, current_user: AnyInternalUser):
    return await trust_center_service.get_document(db, org_id, doc_id)


@router.patch("/documents/{doc_id}", response_model=TrustCenterDocumentResponse)
async def update_document(
    org_id: VerifiedOrgId, doc_id: UUID, data: TrustCenterDocumentUpdate, db: DB, current_user: ComplianceUser
):
    return await trust_center_service.update_document(db, org_id, doc_id, data)


@router.delete("/documents/{doc_id}", status_code=204)
async def delete_document(org_id: VerifiedOrgId, doc_id: UUID, db: DB, current_user: ComplianceUser):
    await trust_center_service.delete_document(db, org_id, doc_id)


# Public route (no auth) — registered separately in router.py
public_router = APIRouter(tags=["trust-center-public"])


@public_router.get("/trust/{slug}", response_model=PublicTrustCenterResponse)
async def get_public_trust_center(slug: str, db: DB):
    result = await trust_center_service.get_public_trust_center(db, slug)
    if not result:
        raise NotFoundError("Trust center not found or not published")
    return result
