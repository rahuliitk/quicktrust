"""Prompt templates for controls generation agent."""

SYSTEM_PROMPT = """You are an expert compliance consultant specializing in GRC (Governance, Risk, and Compliance).
You help companies implement security controls based on compliance frameworks like SOC 2, ISO 27001, and HIPAA.
Your goal is to generate practical, actionable controls tailored to the specific company context."""

CUSTOMIZE_CONTROLS_PROMPT = """Given the following company context and control templates, customize each control
to be specific to this company. Replace generic placeholders with company-specific details.

Company Context:
- Company Name: {company_name}
- Industry: {industry}
- Company Size: {company_size}
- Cloud Providers: {cloud_providers}
- Tech Stack: {tech_stack}

Control Templates to Customize:
{templates_json}

For each template, generate a customized control with:
1. A specific title relevant to the company
2. Customized description mentioning their actual tech stack
3. Implementation details specific to their cloud provider(s)
4. A test procedure tailored to their environment

Return a JSON object with key "controls" containing an array of customized controls.
Each control should have: template_code, title, description, implementation_details,
automation_level, test_procedure, requirement_codes, domain."""

SUGGEST_OWNERS_PROMPT = """Given the following controls and company context, suggest which department
should own each control.

Company Context:
- Departments: {departments}

Controls:
{controls_json}

For each control, suggest the most appropriate department from the available departments.
If no department fits well, suggest "Engineering" or "IT" as defaults.

Return a JSON object with key "assignments" containing an array of objects with
"template_code" and "suggested_owner_department"."""
