from uuid import UUID

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.core.dependencies import DB, AnyInternalUser, ComplianceUser
from app.schemas.common import MessageResponse
from app.services import embedding_service

router = APIRouter(
    prefix="/organizations/{org_id}/embeddings",
    tags=["embeddings"],
)


class SearchRequest(BaseModel):
    query: str
    entity_type: str | None = None
    top_k: int = 10
    min_score: float = 0.3


@router.post("/search")
async def search_similar(
    org_id: UUID, data: SearchRequest, db: DB, current_user: AnyInternalUser,
):
    """Semantic search across controls, policies, evidence, and risks."""
    return await embedding_service.search_similar(
        db, org_id, data.query,
        entity_type=data.entity_type,
        top_k=data.top_k,
        min_score=data.min_score,
    )


@router.post("/index/{entity_type}", response_model=MessageResponse)
async def index_entities(
    org_id: UUID, entity_type: str, db: DB, current_user: ComplianceUser,
):
    """Bulk-index all entities of a given type for semantic search."""
    count = await embedding_service.index_entities(db, org_id, entity_type)
    return MessageResponse(message=f"Indexed {count} {entity_type} entities")
