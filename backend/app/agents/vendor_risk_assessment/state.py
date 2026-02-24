"""State definitions for the vendor risk assessment agent."""
from typing import TypedDict


class VendorRiskAssessmentState(TypedDict, total=False):
    # Input
    org_id: str
    agent_run_id: str
    vendor_id: str

    # Intermediate
    vendor_data: dict
    assessment_criteria: dict
    risk_analysis: dict
    risk_score: int
    recommendations: list[dict]

    # Output
    saved: bool
    error: str | None
