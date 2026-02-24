"""Embedding service for semantic search across controls, policies, and evidence.

Generates text embeddings using a lightweight model and stores them for
similarity search. Falls back gracefully if the sentence-transformers
library is not installed.
"""

import hashlib
import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError
from app.models.embedding import Embedding

logger = logging.getLogger(__name__)

_model = None
_model_available: bool | None = None


def _get_model():
    """Lazily load the sentence-transformers model."""
    global _model, _model_available

    if _model_available is False:
        return None
    if _model is not None:
        return _model

    try:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer("all-MiniLM-L6-v2")
        _model_available = True
        logger.info("Loaded embedding model: all-MiniLM-L6-v2")
        return _model
    except ImportError:
        logger.warning(
            "sentence-transformers not installed. Semantic search will be disabled."
        )
        _model_available = False
        return None


def _compute_embedding(text: str) -> list[float] | None:
    """Compute embedding vector for given text."""
    model = _get_model()
    if model is None:
        return None
    vector = model.encode(text).tolist()
    return vector


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


async def upsert_embedding(
    db: AsyncSession,
    org_id: UUID,
    entity_type: str,
    entity_id: UUID,
    text_content: str,
) -> Embedding | None:
    """Create or update an embedding for an entity."""
    content_hash = hashlib.sha256(text_content.encode()).hexdigest()

    # Check if already up to date
    result = await db.execute(
        select(Embedding).where(
            Embedding.org_id == org_id,
            Embedding.entity_type == entity_type,
            Embedding.entity_id == entity_id,
        )
    )
    existing = result.scalar_one_or_none()

    if existing and existing.content_hash == content_hash:
        return existing  # No change needed

    vector = _compute_embedding(text_content)
    if vector is None:
        return None  # Model not available

    if existing:
        existing.text_content = text_content
        existing.content_hash = content_hash
        existing.vector = vector
        existing.dimensions = len(vector)
        await db.commit()
        await db.refresh(existing)
        return existing

    embedding = Embedding(
        org_id=org_id,
        entity_type=entity_type,
        entity_id=entity_id,
        text_content=text_content,
        content_hash=content_hash,
        vector=vector,
        dimensions=len(vector),
    )
    db.add(embedding)
    await db.commit()
    await db.refresh(embedding)
    return embedding


async def search_similar(
    db: AsyncSession,
    org_id: UUID,
    query_text: str,
    entity_type: str | None = None,
    top_k: int = 10,
    min_score: float = 0.3,
) -> list[dict]:
    """Search for similar entities using cosine similarity.

    Note: For production with PostgreSQL, use pgvector's <=> operator instead
    of in-memory comparison. This implementation works for development with SQLite.
    """
    query_vector = _compute_embedding(query_text)
    if query_vector is None:
        return []

    # Load all embeddings for this org (for SQLite dev; use pgvector in prod)
    base_q = select(Embedding).where(Embedding.org_id == org_id)
    if entity_type:
        base_q = base_q.where(Embedding.entity_type == entity_type)

    result = await db.execute(base_q)
    embeddings = list(result.scalars().all())

    scored = []
    for emb in embeddings:
        if not emb.vector:
            continue
        score = _cosine_similarity(query_vector, emb.vector)
        if score >= min_score:
            scored.append({
                "entity_type": emb.entity_type,
                "entity_id": str(emb.entity_id),
                "text_preview": emb.text_content[:200],
                "similarity_score": round(score, 4),
            })

    scored.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scored[:top_k]


async def index_entities(
    db: AsyncSession, org_id: UUID, entity_type: str
) -> int:
    """Bulk-index all entities of a given type for the organization."""
    from app.models.control import Control
    from app.models.policy import Policy
    from app.models.evidence import Evidence
    from app.models.risk import Risk

    type_map = {
        "control": (Control, lambda c: f"{c.title}. {c.description or ''}"),
        "policy": (Policy, lambda p: f"{p.title}. {p.content[:500] if p.content else ''}"),
        "evidence": (Evidence, lambda e: f"{e.title}. {e.collection_method}"),
        "risk": (Risk, lambda r: f"{r.title}. {r.description or ''} Category: {r.category}"),
    }

    if entity_type not in type_map:
        raise BadRequestError(f"Unknown entity type: {entity_type}")

    model_cls, text_fn = type_map[entity_type]
    result = await db.execute(
        select(model_cls).where(model_cls.org_id == org_id)
    )
    entities = list(result.scalars().all())

    indexed = 0
    for entity in entities:
        text = text_fn(entity)
        if text.strip():
            emb = await upsert_embedding(db, org_id, entity_type, entity.id, text)
            if emb:
                indexed += 1

    return indexed
