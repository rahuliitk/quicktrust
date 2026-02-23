"""Add Phase 6 tables: trust center, reports

Revision ID: 0005_phase6
Revises: 0004_phase5
Create Date: 2026-02-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0005_phase6"
down_revision: Union[str, None] = "0004_phase5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Trust Center Configs ---
    op.create_table(
        "trust_center_configs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False, unique=True),
        sa.Column("is_published", sa.Boolean, server_default="0"),
        sa.Column("slug", sa.String(255), unique=True, nullable=False),
        sa.Column("headline", sa.String(500)),
        sa.Column("description", sa.Text),
        sa.Column("contact_email", sa.String(255)),
        sa.Column("logo_url", sa.String(500)),
        sa.Column("certifications", sa.Text),
        sa.Column("branding", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # --- Trust Center Documents ---
    op.create_table(
        "trust_center_documents",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("document_type", sa.String(100)),
        sa.Column("is_public", sa.Boolean, server_default="0"),
        sa.Column("requires_nda", sa.Boolean, server_default="0"),
        sa.Column("file_url", sa.String(500)),
        sa.Column("description", sa.Text),
        sa.Column("valid_until", sa.DateTime(timezone=True)),
        sa.Column("sort_order", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_trust_center_documents_org_id", "trust_center_documents", ["org_id"])

    # --- Reports ---
    op.create_table(
        "reports",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("report_type", sa.String(50), server_default="compliance_summary"),
        sa.Column("format", sa.String(20), server_default="json"),
        sa.Column("status", sa.String(50), server_default="pending"),
        sa.Column("parameters", sa.Text),
        sa.Column("generated_at", sa.DateTime(timezone=True)),
        sa.Column("file_url", sa.String(500)),
        sa.Column("requested_by_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("error_message", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_reports_org_id", "reports", ["org_id"])


def downgrade() -> None:
    op.drop_table("reports")
    op.drop_table("trust_center_documents")
    op.drop_table("trust_center_configs")
