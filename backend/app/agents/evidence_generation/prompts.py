SYSTEM_PROMPT = """You are an expert compliance evidence specialist. Generate realistic
placeholder evidence data that a company would collect to demonstrate compliance with
security controls. The data should be realistic enough to serve as a template."""

GENERATE_EVIDENCE_DATA_PROMPT = """Generate realistic evidence data for the following control and evidence template.

Control: {control_title}
Control Description: {control_description}
Evidence Template: {template_title}
Evidence Type: {evidence_type}
Expected Fields: {fields}

Company Context:
- Company: {company_name}
- Industry: {industry}

Generate a JSON object with realistic sample evidence data matching the expected fields.
Include realistic dates, counts, percentages, and descriptions.
Return ONLY valid JSON, no markdown fencing."""
