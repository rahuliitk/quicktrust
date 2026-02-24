import logging
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

logger = logging.getLogger(__name__)


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
    """Auto-fill questionnaire using keyword matching (first pass) then LLM (second pass).

    Returns total count of filled answers across both passes.
    """
    questionnaire = await get_questionnaire(db, org_id, questionnaire_id)
    questions = questionnaire.questions or []

    # Load controls and policies for matching
    controls_result = await db.execute(select(Control).where(Control.org_id == org_id))
    controls = list(controls_result.scalars().all())

    policies_result = await db.execute(select(Policy).where(Policy.org_id == org_id))
    policies = list(policies_result.scalars().all())

    filled = 0
    unanswered_questions: list[dict] = []  # questions not matched by keywords

    # ---- Pass 1: keyword matching (existing logic) ----
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
        else:
            # Track for LLM pass
            unanswered_questions.append({
                "id": q_id,
                "text": q.get("text", q.get("question", "")),
            })

    # Commit keyword-matched answers before LLM pass
    if filled > 0:
        questionnaire.answered_count += filled
        if questionnaire.status == "draft":
            questionnaire.status = "in_progress"
        await db.commit()

    # ---- Pass 2: LLM-enhanced auto-fill for remaining questions ----
    if unanswered_questions:
        llm_filled = await _llm_auto_fill(
            db=db,
            org_id=org_id,
            questionnaire_id=questionnaire_id,
            questionnaire=questionnaire,
            unanswered=unanswered_questions,
            controls=controls,
            policies=policies,
        )
        filled += llm_filled

    return filled


async def _llm_auto_fill(
    db: AsyncSession,
    org_id: UUID,
    questionnaire_id: UUID,
    questionnaire: Questionnaire,
    unanswered: list[dict],
    controls: list,
    policies: list,
) -> int:
    """Send unanswered questions to LLM with controls/policies as context.

    Returns count of answers filled by the LLM. Falls back gracefully on error.
    """
    try:
        from app.agents.common.llm import call_llm_json
        from app.services.questionnaire_prompts import (
            SYSTEM_PROMPT,
            build_auto_fill_user_prompt,
        )
    except ImportError:
        logger.warning("LLM module not available; skipping LLM auto-fill pass.")
        return 0

    # Build context strings
    controls_context = "\n".join(
        f"- {ctrl.title} (status: {ctrl.status})"
        + (f" — {ctrl.description[:200]}" if getattr(ctrl, "description", None) else "")
        for ctrl in controls
    ) or "(no controls defined)"

    policies_context = "\n".join(
        f"- {pol.title} (status: {pol.status})"
        + (f" — {pol.description[:200]}" if getattr(pol, "description", None) else "")
        for pol in policies
    ) or "(no policies defined)"

    # Batch questions (max 20 per LLM call to stay within token limits)
    BATCH_SIZE = 20
    total_filled = 0

    for batch_start in range(0, len(unanswered), BATCH_SIZE):
        batch = unanswered[batch_start : batch_start + BATCH_SIZE]

        user_prompt = build_auto_fill_user_prompt(
            questions=batch,
            controls_context=controls_context,
            policies_context=policies_context,
        )

        try:
            llm_result = await call_llm_json(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                max_tokens=4096,
            )
        except Exception as exc:
            logger.warning(
                "LLM auto-fill call failed for batch starting at %d: %s",
                batch_start,
                exc,
            )
            continue  # Skip this batch; keyword results are still saved

        answers = llm_result.get("answers", [])
        batch_filled = 0

        for ans in answers:
            q_id = ans.get("question_id")
            answer_text = ans.get("answer", "")
            confidence = ans.get("confidence", 0.0)
            source_refs = ans.get("source_references", "")

            if not q_id or not answer_text:
                continue

            # Skip very low confidence answers (LLM said it cannot answer)
            if confidence < 0.1:
                continue

            # Find original question text
            original_q = next((q for q in batch if q["id"] == q_id), None)
            if not original_q:
                continue

            response = QuestionnaireResponse(
                questionnaire_id=questionnaire_id,
                org_id=org_id,
                question_id=q_id,
                question_text=original_q["text"],
                answer=answer_text,
                confidence=confidence,
                source_type="llm",
                source_id=None,
            )
            db.add(response)
            batch_filled += 1

        if batch_filled > 0:
            questionnaire.answered_count += batch_filled
            if questionnaire.status == "draft":
                questionnaire.status = "in_progress"
            await db.commit()
            total_filled += batch_filled

    logger.info(
        "LLM auto-fill completed for questionnaire %s: %d answers generated",
        questionnaire_id,
        total_filled,
    )
    return total_filled


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
