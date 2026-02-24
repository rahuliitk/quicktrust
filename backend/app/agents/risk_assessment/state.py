"""State definitions for the risk assessment agent."""
from typing import TypedDict


class RiskAssessmentState(TypedDict, total=False):
    # Input
    org_id: str
    agent_run_id: str
    framework_id: str | None

    # Intermediate
    controls: list[dict]
    identified_risks: list[dict]
    scored_risks: list[dict]

    # Output
    final_risks: list[dict]
    risks_count: int
    error: str | None
