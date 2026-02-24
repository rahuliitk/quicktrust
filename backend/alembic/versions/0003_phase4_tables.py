"""Add Phase 4 tables: training, access reviews

Revision ID: 0003_phase4
Revises: 0002_phase3
Create Date: 2026-02-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003_phase4"
down_revision: Union[str, None] = "0002_phase3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Training Courses ---
    op.create_table(
        "training_courses",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("content_url", sa.String(500)),
        sa.Column("course_type", sa.String(50), server_default="document"),
        sa.Column("required_roles", sa.Text),
        sa.Column("duration_minutes", sa.Integer),
        sa.Column("is_required", sa.Boolean, server_default="0"),
        sa.Column("is_active", sa.Boolean, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_training_courses_org_id", "training_courses", ["org_id"])

    # --- Training Assignments ---
    op.create_table(
        "training_assignments",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("course_id", sa.String(36), sa.ForeignKey("training_courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("status", sa.String(50), server_default="assigned"),
        sa.Column("due_date", sa.DateTime(timezone=True)),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("score", sa.Integer),
        sa.Column("attempts", sa.Integer, server_default="0"),
        sa.Column("assigned_by_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_training_assignments_org_id", "training_assignments", ["org_id"])
    op.create_index("ix_training_assignments_course_id", "training_assignments", ["course_id"])

    # --- Access Review Campaigns ---
    op.create_table(
        "access_review_campaigns",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("reviewer_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("status", sa.String(50), server_default="draft"),
        sa.Column("due_date", sa.DateTime(timezone=True)),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_access_review_campaigns_org_id", "access_review_campaigns", ["org_id"])

    # --- Access Review Entries ---
    op.create_table(
        "access_review_entries",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("campaign_id", sa.String(36), sa.ForeignKey("access_review_campaigns.id", ondelete="CASCADE"), nullable=False),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("user_name", sa.String(255), nullable=False),
        sa.Column("user_email", sa.String(255), nullable=False),
        sa.Column("system_name", sa.String(255), nullable=False),
        sa.Column("resource", sa.String(500)),
        sa.Column("current_access", sa.String(255)),
        sa.Column("decision", sa.String(50)),
        sa.Column("decided_by_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("decided_at", sa.DateTime(timezone=True)),
        sa.Column("notes", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_access_review_entries_campaign_id", "access_review_entries", ["campaign_id"])


def downgrade() -> None:
    op.drop_table("access_review_entries")
    op.drop_table("access_review_campaigns")
    op.drop_table("training_assignments")
    op.drop_table("training_courses")
