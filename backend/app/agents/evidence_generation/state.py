from typing import TypedDict


class EvidenceGenerationState(TypedDict, total=False):
    # Input
    org_id: str
    agent_run_id: str
    company_context: dict

    # Intermediate
    controls: list[dict]
    evidence_templates: list[dict]
    matched_evidence: list[dict]
    generated_evidence: list[dict]

    # Output
    final_evidence: list[dict]
    evidence_count: int
    error: str | None
