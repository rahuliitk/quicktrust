from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB
from app.schemas.common import PaginatedResponse
from app.schemas.policy import PolicyTemplateResponse
from app.services import policy_service

router = APIRouter(prefix="/policy-templates", tags=["policy-templates"])


@router.get("", response_model=PaginatedResponse)
async def list_policy_templates(
    db: DB,
    category: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    templates, total = await policy_service.list_policy_templates(
        db, category=category, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[PolicyTemplateResponse.model_validate(t) for t in templates],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/{template_id}", response_model=PolicyTemplateResponse)
async def get_policy_template(template_id: UUID, db: DB):
    return await policy_service.get_policy_template(db, template_id)
