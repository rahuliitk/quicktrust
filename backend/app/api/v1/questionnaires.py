from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser
from app.schemas.common import PaginatedResponse, MessageResponse
from app.schemas.questionnaire import (
    QuestionnaireCreate,
    QuestionnaireUpdate,
    QuestionnaireDetailResponse,
    QuestionResponseCreate,
    QuestionResponseUpdate,
    QuestionResponseRead,
    QuestionnaireStatsResponse,
)
from app.services import questionnaire_service

router = APIRouter(
    prefix="/organizations/{org_id}/questionnaires",
    tags=["questionnaires"],
)


@router.get("", response_model=PaginatedResponse)
async def list_questionnaires(
    org_id: UUID,
    db: DB,
    current_user: AnyInternalUser,
    status: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await questionnaire_service.list_questionnaires(
        db, org_id, status=status, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[QuestionnaireDetailResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=QuestionnaireDetailResponse, status_code=201)
async def create_questionnaire(org_id: UUID, data: QuestionnaireCreate, db: DB, current_user: ComplianceUser):
    return await questionnaire_service.create_questionnaire(db, org_id, data)


@router.get("/stats", response_model=QuestionnaireStatsResponse)
async def get_stats(org_id: UUID, db: DB, current_user: AnyInternalUser):
    return await questionnaire_service.get_questionnaire_stats(db, org_id)


@router.get("/{questionnaire_id}", response_model=QuestionnaireDetailResponse)
async def get_questionnaire(org_id: UUID, questionnaire_id: UUID, db: DB, current_user: AnyInternalUser):
    return await questionnaire_service.get_questionnaire(db, org_id, questionnaire_id)


@router.patch("/{questionnaire_id}", response_model=QuestionnaireDetailResponse)
async def update_questionnaire(
    org_id: UUID, questionnaire_id: UUID, data: QuestionnaireUpdate, db: DB, current_user: ComplianceUser
):
    return await questionnaire_service.update_questionnaire(db, org_id, questionnaire_id, data)


@router.delete("/{questionnaire_id}", status_code=204)
async def delete_questionnaire(org_id: UUID, questionnaire_id: UUID, db: DB, current_user: ComplianceUser):
    await questionnaire_service.delete_questionnaire(db, org_id, questionnaire_id)


@router.post("/{questionnaire_id}/auto-fill", response_model=MessageResponse)
async def auto_fill(org_id: UUID, questionnaire_id: UUID, db: DB, current_user: ComplianceUser):
    count = await questionnaire_service.auto_fill(db, org_id, questionnaire_id)
    return MessageResponse(message=f"Auto-filled {count} responses")


@router.get("/{questionnaire_id}/responses/{question_id}", response_model=QuestionResponseRead)
async def get_response(
    org_id: UUID, questionnaire_id: UUID, question_id: str, db: DB, current_user: AnyInternalUser
):
    return await questionnaire_service.get_response(db, org_id, questionnaire_id, question_id)


@router.put("/{questionnaire_id}/responses/{question_id}", response_model=QuestionResponseRead)
async def upsert_response(
    org_id: UUID, questionnaire_id: UUID, question_id: str,
    data: QuestionResponseCreate, db: DB, current_user: ComplianceUser,
):
    data.question_id = question_id
    return await questionnaire_service.upsert_response(db, org_id, questionnaire_id, data)


@router.patch("/{questionnaire_id}/responses/{question_id}/approve", response_model=QuestionResponseRead)
async def approve_response(
    org_id: UUID, questionnaire_id: UUID, question_id: str, db: DB, current_user: ComplianceUser
):
    data = QuestionResponseUpdate(is_approved=True)
    return await questionnaire_service.update_response(
        db, org_id, questionnaire_id, question_id, data, approved_by_id=current_user.id
    )
