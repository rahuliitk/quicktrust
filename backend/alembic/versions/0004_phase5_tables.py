"""Add Phase 5 tables: monitoring, questionnaires

Revision ID: 0004_phase5
Revises: 0003_phase4
Create Date: 2026-02-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0004_phase5"
down_revision: Union[str, None] = "0003_phase4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Monitor Rules ---
    op.create_table(
        "monitor_rules",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("control_id", sa.String(36), sa.ForeignKey("controls.id")),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("check_type", sa.String(50), server_default="manual"),
        sa.Column("schedule", sa.String(20), server_default="daily"),
        sa.Column("is_active", sa.Boolean, server_default="1"),
        sa.Column("config", sa.Text),
        sa.Column("last_checked_at", sa.DateTime(timezone=True)),
        sa.Column("last_result", sa.String(20)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_monitor_rules_org_id", "monitor_rules", ["org_id"])

    # --- Monitor Alerts ---
    op.create_table(
        "monitor_alerts",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("rule_id", sa.String(36), sa.ForeignKey("monitor_rules.id", ondelete="CASCADE"), nullable=False),
        sa.Column("severity", sa.String(20), server_default="medium"),
        sa.Column("status", sa.String(50), server_default="open"),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("details", sa.Text),
        sa.Column("triggered_at", sa.DateTime(timezone=True)),
        sa.Column("resolved_at", sa.DateTime(timezone=True)),
        sa.Column("acknowledged_by_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_monitor_alerts_org_id", "monitor_alerts", ["org_id"])
    op.create_index("ix_monitor_alerts_rule_id", "monitor_alerts", ["rule_id"])

    # --- Questionnaires ---
    op.create_table(
        "questionnaires",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("source", sa.String(255)),
        sa.Column("status", sa.String(50), server_default="draft"),
        sa.Column("questions", sa.Text),
        sa.Column("total_questions", sa.Integer, server_default="0"),
        sa.Column("answered_count", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_questionnaires_org_id", "questionnaires", ["org_id"])

    # --- Questionnaire Responses ---
    op.create_table(
        "questionnaire_responses",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("questionnaire_id", sa.String(36), sa.ForeignKey("questionnaires.id", ondelete="CASCADE"), nullable=False),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("question_id", sa.String(100), nullable=False),
        sa.Column("question_text", sa.Text, nullable=False),
        sa.Column("answer", sa.Text),
        sa.Column("confidence", sa.Float),
        sa.Column("source_type", sa.String(50)),
        sa.Column("source_id", sa.String(36)),
        sa.Column("is_approved", sa.Boolean, server_default="0"),
        sa.Column("approved_by_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_questionnaire_responses_questionnaire_id", "questionnaire_responses", ["questionnaire_id"])


def downgrade() -> None:
    op.drop_table("questionnaire_responses")
    op.drop_table("questionnaires")
    op.drop_table("monitor_alerts")
    op.drop_table("monitor_rules")
