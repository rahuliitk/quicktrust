"""State definitions for the controls generation agent."""
from typing import TypedDict


class CompanyContext(TypedDict, total=False):
    name: str
    industry: str
    company_size: str
    cloud_providers: list[str]
    tech_stack: list[str]
    departments: list[str]
    special_requirements: str


class ControlDraft(TypedDict, total=False):
    template_code: str
    title: str
    description: str
    implementation_details: str
    automation_level: str
    test_procedure: str
    suggested_owner_department: str
    requirement_codes: list[str]
    domain: str


class ControlsGenerationState(TypedDict, total=False):
    # Input
    org_id: str
    agent_run_id: str
    framework_id: str
    company_context: CompanyContext

    # Intermediate
    requirements: list[dict]
    templates: list[dict]
    matched_templates: list[dict]
    customized_controls: list[ControlDraft]
    deduplicated_controls: list[ControlDraft]
    controls_with_owners: list[ControlDraft]

    # Output
    final_controls: list[dict]
    controls_count: int
    error: str | None
