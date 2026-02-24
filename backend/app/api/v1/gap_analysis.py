from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import DB, AnyInternalUser
from app.services import gap_analysis_service

router = APIRouter(
    prefix="/organizations/{org_id}/gap-analysis",
    tags=["gap-analysis"],
)


@router.get("/framework/{framework_id}")
async def get_gap_analysis(
    org_id: UUID, framework_id: UUID, db: DB, current_user: AnyInternalUser,
):
    """Get gap analysis for a specific framework — shows covered, partial, and missing requirements."""
    return await gap_analysis_service.get_gap_analysis(db, org_id, framework_id)


@router.get("/cross-framework")
async def get_cross_framework_matrix(
    org_id: UUID, db: DB, current_user: AnyInternalUser,
):
    """Get cross-framework control mapping matrix with deduplication opportunities."""
    return await gap_analysis_service.get_cross_framework_matrix(db, org_id)
