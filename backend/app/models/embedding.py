"""Vector embeddings model for semantic search in agent memory.

Uses a JSON-serialized float array for SQLite compatibility.
On PostgreSQL with pgvector, swap JSONType for Vector(dimensions).
"""

import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel, GUID, JSONType


class Embedding(BaseModel):
    __tablename__ = "embeddings"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    entity_type: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # control, policy, evidence, risk
    entity_id: Mapped[uuid.UUID] = mapped_column(GUID(), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    text_content: Mapped[str] = mapped_column(Text, nullable=False)
    vector: Mapped[list | None] = mapped_column(
        JSONType(), default=list
    )  # float[] stored as JSON; use pgvector in prod
    dimensions: Mapped[int] = mapped_column(Integer, default=384)
    model_name: Mapped[str] = mapped_column(
        String(100), default="all-MiniLM-L6-v2"
    )
