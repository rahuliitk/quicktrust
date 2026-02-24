from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.questionnaire import Questionnaire, QuestionnaireResponse
from app.models.control import Control
from app.models.policy import Policy
from app.schemas.questionnaire import (
    QuestionnaireCreate, QuestionnaireUpdate,
    QuestionResponseCreate, QuestionResponseUpdate,
)


async def list_questionnaires(
    db: AsyncSession,
    org_id: UUID,
    status: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[Questionnaire], int]:
    base_q = select(Questionnaire).where(Questionnaire.org_id == org_id)
    count_q = select(func.count()).select_from(Questionnaire).where(Questionnaire.org_id == org_id)

    if status:
        base_q = base_q.where(Questionnaire.status == status)
        count_q = count_q.where(Questionnaire.status == status)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(Questionnaire.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_questionnaire(db: AsyncSession, org_id: UUID, data: QuestionnaireCreate) -> Questionnaire:
    fields = data.model_dump()
    questions = fields.get("questions") or []
    questionnaire = Questionnaire(
        org_id=org_id,
        total_questions=len(questions),
        **fields,
    )
    db.add(questionnaire)
    await db.commit()
    await db.refresh(questionnaire)
    return questionnaire


async def get_questionnaire(db: AsyncSession, org_id: UUID, questionnaire_id: UUID) -> Questionnaire:
    result = await db.execute(
        select(Questionnaire).where(
            Questionnaire.id == questionnaire_id, Questionnaire.org_id == org_id
        )
    )
    questionnaire = result.scalar_one_or_none()
    if not questionnaire:
        raise NotFoundError(f"Questionnaire {questionnaire_id} not found")
    return questionnaire


async def update_questionnaire(
    db: AsyncSession, org_id: UUID, questionnaire_id: UUID, data: QuestionnaireUpdate
) -> Questionnaire:
    questionnaire = await get_questionnaire(db, org_id, questionnaire_id)
    update_data = data.model_dump(exclude_unset=True)

    if "questions" in update_data and update_data["questions"] is not None:
        update_data["total_questions"] = len(update_data["questions"])

    for field, value in update_data.items():
        setattr(questionnaire, field, value)
    await db.commit()
    await db.refresh(questionnaire)
    return questionnaire


async def delete_questionnaire(db: AsyncSession, org_id: UUID, questionnaire_id: UUID) -> None:
    questionnaire = await get_questionnaire(db, org_id, questionnaire_id)
    await db.delete(questionnaire)
    await db.commit()


# === Responses ===

async def upsert_response(
    db: AsyncSession, org_id: UUID, questionnaire_id: UUID, data: QuestionResponseCreate
) -> QuestionnaireResponse:
    await get_questionnaire(db, org_id, questionnaire_id)

    # Check if response already exists for this question_id
    result = await db.execute(
        select(QuestionnaireResponse).where(
            QuestionnaireResponse.questionnaire_id == questionnaire_id,
            QuestionnaireResponse.question_id == data.question_id,
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(existing, field, value)
        await db.commit()
        await db.refresh(existing)
        return existing

    response = QuestionnaireResponse(
        questionnaire_id=questionnaire_id,
        org_id=org_id,
        **data.model_dump(),
    )
    db.add(response)

    # Update answered count
    questionnaire = await get_questionnaire(db, org_id, questionnaire_id)
    questionnaire.answered_count += 1

    await db.commit()
    await db.refresh(response)
    return response


async def get_response(
    db: AsyncSession, org_id: UUID, questionnaire_id: UUID, question_id: str
) -> QuestionnaireResponse:
    result = await db.execute(
        select(QuestionnaireResponse).where(
            QuestionnaireResponse.questionnaire_id == questionnaire_id,
            QuestionnaireResponse.question_id == question_id,
        )
    )
    response = result.scalar_one_or_none()
    if not response:
        raise NotFoundError(f"Response for question {question_id} not found")
    return response


async def update_response(
    db: AsyncSession, org_id: UUID, questionnaire_id: UUID, question_id: str,
    data: QuestionResponseUpdate, approved_by_id: UUID | None = None,
) -> QuestionnaireResponse:
    response = await get_response(db, org_id, questionnaire_id, question_id)
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(response, field, value)

    if "is_approved" in update_data and update_data["is_approved"]:
        response.approved_by_id = approved_by_id

    await db.commit()
    await db.refresh(response)
    return response


# === Auto-Fill ===

async def auto_fill(db: AsyncSession, org_id: UUID, questionnaire_id: UUID) -> int:
    """Scan question text for keyword matches against control/policy titles. Returns count of filled answers."""
    questionnaire = await get_questionnaire(db, org_id, questionnaire_id)
    questions = questionnaire.questions or []

    # Load controls and policies for matching
    controls_result = await db.execute(select(Control).where(Control.org_id == org_id))
    controls = list(controls_result.scalars().all())

    policies_result = await db.execute(select(Policy).where(Policy.org_id == org_id))
    policies = list(policies_result.scalars().all())

    filled = 0
    for idx, q in enumerate(questions):
        q_id = q.get("id", f"q_{idx}")
        q_text = q.get("text", q.get("question", "")).lower()
        if not q_text:
            continue

        # Check if already answered
        existing = await db.execute(
            select(QuestionnaireResponse).where(
                QuestionnaireResponse.questionnaire_id == questionnaire_id,
                QuestionnaireResponse.question_id == q_id,
            )
        )
        if existing.scalar_one_or_none():
            continue

        # Try to match against controls
        best_match = None
        best_source = None
        for ctrl in controls:
            if ctrl.title and ctrl.title.lower() in q_text:
                best_match = f"Yes — covered by control: {ctrl.title}. Status: {ctrl.status}."
                best_source = ("control", ctrl.id)
                break
            # Check keywords
            title_words = (ctrl.title or "").lower().split()
            matches = sum(1 for w in title_words if len(w) > 3 and w in q_text)
            if matches >= 2 and not best_match:
                best_match = f"Partially addressed by control: {ctrl.title}."
                best_source = ("control", ctrl.id)

        # Try to match against policies
        if not best_match:
            for pol in policies:
                if pol.title and pol.title.lower() in q_text:
                    best_match = f"Yes — addressed in policy: {pol.title}. Status: {pol.status}."
                    best_source = ("policy", pol.id)
                    break

        if best_match and best_source:
            response = QuestionnaireResponse(
                questionnaire_id=questionnaire_id,
                org_id=org_id,
                question_id=q_id,
                question_text=q.get("text", q.get("question", "")),
                answer=best_match,
                confidence=0.7,
                source_type=best_source[0],
                source_id=best_source[1],
            )
            db.add(response)
            filled += 1

    if filled > 0:
        questionnaire.answered_count += filled
        if questionnaire.status == "draft":
            questionnaire.status = "in_progress"
        await db.commit()

    return filled


# === Stats ===

async def get_questionnaire_stats(db: AsyncSession, org_id: UUID) -> dict:
    result = await db.execute(select(Questionnaire).where(Questionnaire.org_id == org_id))
    questionnaires = list(result.scalars().all())

    by_status: dict[str, int] = {}
    for q in questionnaires:
        by_status[q.status] = by_status.get(q.status, 0) + 1

    return {
        "total": len(questionnaires),
        "draft": by_status.get("draft", 0),
        "in_progress": by_status.get("in_progress", 0),
        "completed": by_status.get("completed", 0),
        "submitted": by_status.get("submitted", 0),
    }
