from uuid import UUID

from fastapi import APIRouter, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import DB
from app.core.exceptions import NotFoundError
from app.models.control_template import ControlTemplate
from app.schemas.common import PaginatedResponse
from app.schemas.control_template import ControlTemplateBriefResponse, ControlTemplateResponse

router = APIRouter(prefix="/control-templates", tags=["control-templates"])


@router.get("", response_model=PaginatedResponse)
async def list_control_templates(
    db: DB,
    domain: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    base_q = select(ControlTemplate)
    count_q = select(func.count()).select_from(ControlTemplate)

    if domain:
        base_q = base_q.where(ControlTemplate.domain == domain)
        count_q = count_q.where(ControlTemplate.domain == domain)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(ControlTemplate.domain)
    result = await db.execute(q)
    items = [ControlTemplateBriefResponse.model_validate(t) for t in result.scalars().all()]

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/{template_id}", response_model=ControlTemplateResponse)
async def get_control_template(template_id: UUID, db: DB):
    result = await db.execute(
        select(ControlTemplate).where(ControlTemplate.id == template_id)
    )
    template = result.scalar_one_or_none()
    if not template:
        raise NotFoundError(f"Control template {template_id} not found")
    return template
