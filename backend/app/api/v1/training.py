from uuid import UUID

from fastapi import APIRouter, Query

from app.core.audit_middleware import log_audit
from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.schemas.common import PaginatedResponse
from app.schemas.training import (
    TrainingCourseCreate,
    TrainingCourseUpdate,
    TrainingCourseResponse,
    TrainingAssignmentCreate,
    TrainingAssignmentUpdate,
    TrainingAssignmentResponse,
    TrainingStatsResponse,
)
from app.services import training_service

router = APIRouter(
    prefix="/organizations/{org_id}/training",
    tags=["training"],
)


# === Courses ===

@router.get("/courses", response_model=PaginatedResponse)
async def list_courses(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    is_active: bool | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await training_service.list_courses(
        db, org_id, is_active=is_active, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[TrainingCourseResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("/courses", response_model=TrainingCourseResponse, status_code=201)
async def create_course(org_id: VerifiedOrgId, data: TrainingCourseCreate, db: DB, current_user: ComplianceUser):
    item = await training_service.create_course(db, org_id, data)
    await log_audit(db, current_user, "create", "training_course", str(item.id), org_id)
    return item


@router.get("/courses/{course_id}", response_model=TrainingCourseResponse)
async def get_course(org_id: VerifiedOrgId, course_id: UUID, db: DB, current_user: AnyInternalUser):
    return await training_service.get_course(db, org_id, course_id)


@router.patch("/courses/{course_id}", response_model=TrainingCourseResponse)
async def update_course(
    org_id: VerifiedOrgId, course_id: UUID, data: TrainingCourseUpdate, db: DB, current_user: ComplianceUser
):
    item = await training_service.update_course(db, org_id, course_id, data)
    await log_audit(db, current_user, "update", "training_course", str(course_id), org_id)
    return item


@router.delete("/courses/{course_id}", status_code=204)
async def delete_course(org_id: VerifiedOrgId, course_id: UUID, db: DB, current_user: ComplianceUser):
    await training_service.delete_course(db, org_id, course_id)
    await log_audit(db, current_user, "delete", "training_course", str(course_id), org_id)


# === Assignments ===

@router.get("/assignments", response_model=PaginatedResponse)
async def list_assignments(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    course_id: UUID | None = None,
    status: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await training_service.list_assignments(
        db, org_id, course_id=course_id, status=status, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[TrainingAssignmentResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("/assignments", response_model=TrainingAssignmentResponse, status_code=201)
async def create_assignment(org_id: VerifiedOrgId, data: TrainingAssignmentCreate, db: DB, current_user: ComplianceUser):
    item = await training_service.create_assignment(db, org_id, data, assigned_by_id=current_user.id)
    await log_audit(db, current_user, "create", "training_assignment", str(item.id), org_id)
    return item


@router.get("/assignments/stats", response_model=TrainingStatsResponse)
async def get_training_stats(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    return await training_service.get_training_stats(db, org_id)


@router.patch("/assignments/{assignment_id}", response_model=TrainingAssignmentResponse)
async def update_assignment(
    org_id: VerifiedOrgId, assignment_id: UUID, data: TrainingAssignmentUpdate, db: DB, current_user: CurrentUser
):
    item = await training_service.update_assignment(db, org_id, assignment_id, data)
    await log_audit(db, current_user, "update", "training_assignment", str(assignment_id), org_id)
    return item
