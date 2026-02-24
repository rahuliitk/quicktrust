"""Add Phase 3 tables: incidents, vendors

Revision ID: 0002_phase3
Revises: 0001_phase2
Create Date: 2026-02-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_phase3"
down_revision: Union[str, None] = "0001_phase2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Incidents ---
    op.create_table(
        "incidents",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("severity", sa.String(20), server_default="P3"),
        sa.Column("status", sa.String(50), server_default="open"),
        sa.Column("category", sa.String(100)),
        sa.Column("assigned_to_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("detected_at", sa.DateTime(timezone=True)),
        sa.Column("resolved_at", sa.DateTime(timezone=True)),
        sa.Column("post_mortem_notes", sa.Text),
        sa.Column("related_control_ids", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_incidents_org_id", "incidents", ["org_id"])
    op.create_index("ix_incidents_status", "incidents", ["status"])
    op.create_index("ix_incidents_severity", "incidents", ["severity"])

    # --- Incident Timeline Events ---
    op.create_table(
        "incident_timeline_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("incident_id", sa.String(36), sa.ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("actor_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_incident_timeline_events_incident_id", "incident_timeline_events", ["incident_id"])

    # --- Vendors ---
    op.create_table(
        "vendors",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("name", sa.String(500), nullable=False),
        sa.Column("category", sa.String(100)),
        sa.Column("website", sa.String(500)),
        sa.Column("risk_tier", sa.String(20), server_default="medium"),
        sa.Column("status", sa.String(50), server_default="active"),
        sa.Column("contact_name", sa.String(255)),
        sa.Column("contact_email", sa.String(255)),
        sa.Column("contract_start_date", sa.DateTime(timezone=True)),
        sa.Column("contract_end_date", sa.DateTime(timezone=True)),
        sa.Column("last_assessment_date", sa.DateTime(timezone=True)),
        sa.Column("next_assessment_date", sa.DateTime(timezone=True)),
        sa.Column("assessment_score", sa.Integer),
        sa.Column("notes", sa.Text),
        sa.Column("tags", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_vendors_org_id", "vendors", ["org_id"])
    op.create_index("ix_vendors_risk_tier", "vendors", ["risk_tier"])
    op.create_index("ix_vendors_status", "vendors", ["status"])

    # --- Vendor Assessments ---
    op.create_table(
        "vendor_assessments",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("vendor_id", sa.String(36), sa.ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("assessed_by_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("assessment_date", sa.DateTime(timezone=True)),
        sa.Column("score", sa.Integer),
        sa.Column("risk_tier_assigned", sa.String(20)),
        sa.Column("notes", sa.Text),
        sa.Column("questionnaire_data", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_vendor_assessments_vendor_id", "vendor_assessments", ["vendor_id"])


def downgrade() -> None:
    op.drop_table("vendor_assessments")
    op.drop_table("vendors")
    op.drop_table("incident_timeline_events")
    op.drop_table("incidents")
