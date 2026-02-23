"""Add Phase 2 tables: risks, integrations, audits, onboarding

Revision ID: 0001_phase2
Revises: None
Create Date: 2026-02-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0001_phase2"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Risks ---
    op.create_table(
        "risks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("category", sa.String(50), server_default="operational"),
        sa.Column("likelihood", sa.Integer, server_default="3"),
        sa.Column("impact", sa.Integer, server_default="3"),
        sa.Column("risk_score", sa.Integer, server_default="9"),
        sa.Column("risk_level", sa.String(20), server_default="medium"),
        sa.Column("status", sa.String(50), server_default="identified"),
        sa.Column("treatment_plan", sa.Text),
        sa.Column("treatment_type", sa.String(50)),
        sa.Column("treatment_status", sa.String(50)),
        sa.Column("treatment_due_date", sa.DateTime(timezone=True)),
        sa.Column("residual_likelihood", sa.Integer),
        sa.Column("residual_impact", sa.Integer),
        sa.Column("residual_score", sa.Integer),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("reviewer_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("last_review_date", sa.DateTime(timezone=True)),
        sa.Column("next_review_date", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_risks_org_id", "risks", ["org_id"])

    # --- Risk-Control Mappings ---
    op.create_table(
        "risk_control_mappings",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("risk_id", sa.String(36), sa.ForeignKey("risks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("control_id", sa.String(36), sa.ForeignKey("controls.id", ondelete="CASCADE"), nullable=False),
        sa.Column("effectiveness", sa.String(50), server_default="partially_mitigates"),
        sa.Column("notes", sa.Text),
    )
    op.create_index("ix_risk_control_mappings_risk_id", "risk_control_mappings", ["risk_id"])
    op.create_index("ix_risk_control_mappings_control_id", "risk_control_mappings", ["control_id"])

    # --- Integrations ---
    op.create_table(
        "integrations",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("provider", sa.String(50), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("status", sa.String(50), server_default="connected"),
        sa.Column("config", sa.Text),  # JSON stored as text
        sa.Column("credentials_ref", sa.String(500)),
        sa.Column("last_sync_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_integrations_org_id", "integrations", ["org_id"])

    # --- Collection Jobs ---
    op.create_table(
        "collection_jobs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("integration_id", sa.String(36), sa.ForeignKey("integrations.id"), nullable=False),
        sa.Column("evidence_template_id", sa.String(36), sa.ForeignKey("evidence_templates.id")),
        sa.Column("control_id", sa.String(36), sa.ForeignKey("controls.id")),
        sa.Column("status", sa.String(50), server_default="pending"),
        sa.Column("collector_type", sa.String(100), nullable=False),
        sa.Column("result_data", sa.Text),  # JSON stored as text
        sa.Column("evidence_id", sa.String(36)),
        sa.Column("error_message", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_collection_jobs_org_id", "collection_jobs", ["org_id"])

    # --- Audits ---
    op.create_table(
        "audits",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("framework_id", sa.String(36), sa.ForeignKey("frameworks.id")),
        sa.Column("audit_type", sa.String(50), server_default="external"),
        sa.Column("status", sa.String(50), server_default="planning"),
        sa.Column("auditor_firm", sa.String(255)),
        sa.Column("lead_auditor_name", sa.String(255)),
        sa.Column("scheduled_start", sa.DateTime(timezone=True)),
        sa.Column("scheduled_end", sa.DateTime(timezone=True)),
        sa.Column("readiness_score", sa.Float),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_audits_org_id", "audits", ["org_id"])

    # --- Audit Findings ---
    op.create_table(
        "audit_findings",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("audit_id", sa.String(36), sa.ForeignKey("audits.id", ondelete="CASCADE"), nullable=False),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("control_id", sa.String(36), sa.ForeignKey("controls.id")),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("severity", sa.String(50), server_default="medium"),
        sa.Column("status", sa.String(50), server_default="open"),
        sa.Column("remediation_plan", sa.Text),
        sa.Column("remediation_due_date", sa.DateTime(timezone=True)),
        sa.Column("remediation_owner_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_audit_findings_audit_id", "audit_findings", ["audit_id"])

    # --- Auditor Access Tokens ---
    op.create_table(
        "auditor_access_tokens",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("audit_id", sa.String(36), sa.ForeignKey("audits.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(128), unique=True, nullable=False),
        sa.Column("auditor_email", sa.String(255), nullable=False),
        sa.Column("auditor_name", sa.String(255)),
        sa.Column("permissions", sa.Text),  # JSON stored as text
        sa.Column("is_active", sa.Boolean, server_default="1"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_auditor_access_tokens_audit_id", "auditor_access_tokens", ["audit_id"])
    op.create_index("ix_auditor_access_tokens_token_hash", "auditor_access_tokens", ["token_hash"], unique=True)

    # --- Onboarding Sessions ---
    op.create_table(
        "onboarding_sessions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("status", sa.String(50), server_default="in_progress"),
        sa.Column("input_data", sa.Text),  # JSON stored as text
        sa.Column("progress", sa.Text),  # JSON stored as text
        sa.Column("results", sa.Text),  # JSON stored as text
        sa.Column("agent_run_ids", sa.Text),  # JSON stored as text
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_onboarding_sessions_org_id", "onboarding_sessions", ["org_id"])


def downgrade() -> None:
    op.drop_table("onboarding_sessions")
    op.drop_table("auditor_access_tokens")
    op.drop_table("audit_findings")
    op.drop_table("audits")
    op.drop_table("collection_jobs")
    op.drop_table("integrations")
    op.drop_table("risk_control_mappings")
    op.drop_table("risks")
