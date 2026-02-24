"""State definitions for the audit preparation agent."""
from typing import TypedDict


class AuditPreparationState(TypedDict, total=False):
    # Input
    org_id: str
    agent_run_id: str
    audit_id: str

    # Intermediate
    framework_id: str | None
    controls: list[dict]
    evidence: list[dict]
    gaps: list[dict]
    workpapers: list[dict]

    # Output
    readiness_assessment: dict
    error: str | None
