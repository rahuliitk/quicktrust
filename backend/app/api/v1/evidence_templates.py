from uuid import UUID

from fastapi import APIRouter, Query
from sqlalchemy import select, func

from app.core.dependencies import DB
from app.core.exceptions import NotFoundError
from app.models.evidence_template import EvidenceTemplate
from app.schemas.common import PaginatedResponse
from app.schemas.evidence_template import EvidenceTemplateBriefResponse, EvidenceTemplateResponse

router = APIRouter(prefix="/evidence-templates", tags=["evidence-templates"])


@router.get("", response_model=PaginatedResponse)
async def list_evidence_templates(
    db: DB,
    evidence_type: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    base_q = select(EvidenceTemplate)
    count_q = select(func.count()).select_from(EvidenceTemplate)

    if evidence_type:
        base_q = base_q.where(EvidenceTemplate.evidence_type == evidence_type)
        count_q = count_q.where(EvidenceTemplate.evidence_type == evidence_type)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(EvidenceTemplate.template_code)
    result = await db.execute(q)
    items = [EvidenceTemplateBriefResponse.model_validate(t) for t in result.scalars().all()]

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/{template_id}", response_model=EvidenceTemplateResponse)
async def get_evidence_template(template_id: UUID, db: DB):
    result = await db.execute(
        select(EvidenceTemplate).where(EvidenceTemplate.id == template_id)
    )
    template = result.scalar_one_or_none()
    if not template:
        raise NotFoundError(f"Evidence template {template_id} not found")
    return template
