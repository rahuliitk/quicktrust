from typing import TypedDict


class PolicyDraft(TypedDict, total=False):
    template_code: str
    title: str
    content: str
    category: str
    framework_ids: list[str]
    control_ids: list[str]
    sections: list[str]


class PolicyGenerationState(TypedDict, total=False):
    # Input
    org_id: str
    agent_run_id: str
    framework_id: str
    company_context: dict

    # Intermediate
    controls: list[dict]
    policies_needed: list[dict]
    matched_templates: list[dict]
    generated_policies: list[PolicyDraft]

    # Output
    final_policies: list[dict]
    policies_count: int
    error: str | None
