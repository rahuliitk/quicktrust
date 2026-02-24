"""Add v0.5 tables: notifications, auditor_profiles, embeddings, slack_webhook_configs

Revision ID: 0006_v05
Revises: 0005_phase6
Create Date: 2026-02-24

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0006_v05"
down_revision: Union[str, None] = "0005_phase6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "notifications",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("channel", sa.String(50), server_default="in_app"),
        sa.Column("category", sa.String(100), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("message", sa.Text),
        sa.Column("severity", sa.String(20), server_default="info"),
        sa.Column("entity_type", sa.String(100)),
        sa.Column("entity_id", sa.String(36)),
        sa.Column("is_read", sa.Boolean, server_default=sa.text("0")),
        sa.Column("read_at", sa.DateTime(timezone=True)),
        sa.Column("sent_at", sa.DateTime(timezone=True)),
        sa.Column("metadata_json", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "notification_preferences",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("channel", sa.String(50), nullable=False),
        sa.Column("categories", sa.Text),
        sa.Column("is_enabled", sa.Boolean, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "slack_webhook_configs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("webhook_url", sa.String(1000), nullable=False),
        sa.Column("channel_name", sa.String(100)),
        sa.Column("categories", sa.Text),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "auditor_profiles",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False, unique=True),
        sa.Column("firm_name", sa.String(255)),
        sa.Column("bio", sa.Text),
        sa.Column("credentials", sa.Text),  # JSON
        sa.Column("specializations", sa.Text),  # JSON
        sa.Column("years_experience", sa.Integer),
        sa.Column("location", sa.String(255)),
        sa.Column("hourly_rate", sa.Float),
        sa.Column("is_verified", sa.Boolean, server_default=sa.text("0")),
        sa.Column("rating", sa.Float),
        sa.Column("total_audits", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "embeddings",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("entity_type", sa.String(50), nullable=False),
        sa.Column("entity_id", sa.String(36), nullable=False),
        sa.Column("content_hash", sa.String(64)),
        sa.Column("text_content", sa.Text),
        sa.Column("vector", sa.Text),  # JSON array; use pgvector in production
        sa.Column("dimensions", sa.Integer),
        sa.Column("model_name", sa.String(100)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )


def downgrade() -> None:
    op.drop_table("embeddings")
    op.drop_table("auditor_profiles")
    op.drop_table("slack_webhook_configs")
    op.drop_table("notification_preferences")
    op.drop_table("notifications")
