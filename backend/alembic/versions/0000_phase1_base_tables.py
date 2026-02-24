"""Create Phase 1 base tables: organizations, users, frameworks, controls, evidence, policies, agents, audit_logs

Revision ID: 0000_phase1
Revises: None
Create Date: 2026-02-24

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0000_phase1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Organizations ---
    op.create_table(
        "organizations",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("industry", sa.String(100)),
        sa.Column("company_size", sa.String(50)),
        sa.Column("cloud_providers", sa.Text),  # JSON
        sa.Column("tech_stack", sa.Text),  # JSON
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    # --- Users ---
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("keycloak_id", sa.String(255), unique=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255)),
        sa.Column("role", sa.String(50), server_default="employee"),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    # --- Frameworks ---
    op.create_table(
        "frameworks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id")),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("version", sa.String(50)),
        sa.Column("description", sa.Text),
        sa.Column("category", sa.String(100)),
        sa.Column("is_custom", sa.Boolean, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    # --- Framework Domains ---
    op.create_table(
        "framework_domains",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("framework_id", sa.String(36), sa.ForeignKey("frameworks.id"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("domain_order", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    # --- Framework Requirements ---
    op.create_table(
        "framework_requirements",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("domain_id", sa.String(36), sa.ForeignKey("framework_domains.id"), nullable=False),
        sa.Column("ref_code", sa.String(50)),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    # --- Control Objectives ---
    op.create_table(
        "control_objectives",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("requirement_id", sa.String(36), sa.ForeignKey("framework_requirements.id"), nullable=False),
        sa.Column("ref_code", sa.String(50)),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    # --- Control Templates ---
    op.create_table(
        "control_templates",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("implementation_guidance", sa.Text),
        sa.Column("domain", sa.String(100)),
        sa.Column("category", sa.String(100)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    # --- Evidence Templates ---
    op.create_table(
        "evidence_templates",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("evidence_type", sa.String(50)),
        sa.Column("collection_method", sa.String(50)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    # --- Controls ---
    op.create_table(
        "controls",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("template_id", sa.String(36), sa.ForeignKey("control_templates.id")),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("status", sa.String(50), server_default="draft"),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("implementation_notes", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    # --- Evidence ---
    op.create_table(
        "evidence",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("control_id", sa.String(36), sa.ForeignKey("controls.id")),
        sa.Column("template_id", sa.String(36), sa.ForeignKey("evidence_templates.id")),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("status", sa.String(50), server_default="pending"),
        sa.Column("collection_method", sa.String(50), server_default="manual"),
        sa.Column("collector", sa.String(100)),
        sa.Column("collected_at", sa.DateTime(timezone=True)),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
        sa.Column("file_url", sa.String(1000)),
        sa.Column("file_name", sa.String(500)),
        sa.Column("artifact_hash", sa.String(64)),
        sa.Column("data", sa.Text),  # JSON
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    # --- Policies ---
    op.create_table(
        "policies",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("content", sa.Text),
        sa.Column("status", sa.String(50), server_default="draft"),
        sa.Column("category", sa.String(100)),
        sa.Column("approved_by_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("approved_at", sa.DateTime(timezone=True)),
        sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.Column("next_review_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    # --- Policy Templates ---
    op.create_table(
        "policy_templates",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("content", sa.Text),
        sa.Column("category", sa.String(100)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    # --- Agent Runs ---
    op.create_table(
        "agent_runs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("agent_type", sa.String(100), nullable=False),
        sa.Column("status", sa.String(50), server_default="pending"),
        sa.Column("input_data", sa.Text),  # JSON
        sa.Column("output_data", sa.Text),  # JSON
        sa.Column("error_message", sa.Text),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    # --- Audit Logs ---
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id")),
        sa.Column("actor_id", sa.String(36)),
        sa.Column("actor_type", sa.String(50), server_default="user"),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("entity_type", sa.String(100)),
        sa.Column("entity_id", sa.String(36)),
        sa.Column("changes", sa.Text),  # JSON
        sa.Column("ip_address", sa.String(45)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # --- Control-Framework Mappings ---
    op.create_table(
        "control_framework_mappings",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("control_id", sa.String(36), sa.ForeignKey("controls.id"), nullable=False),
        sa.Column("framework_id", sa.String(36), sa.ForeignKey("frameworks.id")),
        sa.Column("requirement_id", sa.String(36), sa.ForeignKey("framework_requirements.id")),
        sa.Column("objective_id", sa.String(36), sa.ForeignKey("control_objectives.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    # --- Control Template Framework Mappings ---
    op.create_table(
        "control_template_framework_mappings",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("control_template_id", sa.String(36), sa.ForeignKey("control_templates.id"), nullable=False),
        sa.Column("framework_id", sa.String(36), sa.ForeignKey("frameworks.id")),
        sa.Column("requirement_id", sa.String(36), sa.ForeignKey("framework_requirements.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
    )


def downgrade() -> None:
    op.drop_table("control_template_framework_mappings")
    op.drop_table("control_framework_mappings")
    op.drop_table("audit_logs")
    op.drop_table("agent_runs")
    op.drop_table("policy_templates")
    op.drop_table("policies")
    op.drop_table("evidence")
    op.drop_table("controls")
    op.drop_table("evidence_templates")
    op.drop_table("control_templates")
    op.drop_table("control_objectives")
    op.drop_table("framework_requirements")
    op.drop_table("framework_domains")
    op.drop_table("frameworks")
    op.drop_table("users")
    op.drop_table("organizations")
