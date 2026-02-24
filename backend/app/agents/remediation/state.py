"""State definitions for the remediation agent."""
from typing import TypedDict


class RemediationState(TypedDict, total=False):
    # Input
    org_id: str
    agent_run_id: str

    # Intermediate
    failing_controls: list[dict]
    remediation_plans: list[dict]
    prioritized_plans: list[dict]

    # Output
    saved_count: int
    error: str | None
