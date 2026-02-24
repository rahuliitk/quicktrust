"""Prompt templates for the risk assessment agent."""

SYSTEM_PROMPT = """You are an expert risk analyst specializing in information security and compliance.
You assess organizational risk posture by examining controls, identifying coverage gaps, and evaluating
threats based on industry best practices including ISO 31000, NIST RMF, and COSO ERM frameworks.
Your analysis is thorough, actionable, and calibrated to real-world threat landscapes."""

IDENTIFY_RISKS_PROMPT = """Analyze the following set of organizational controls and their current statuses.
Identify potential risk areas where the organization may be exposed.

Controls:
{controls_json}

For each identified risk, provide:
1. A clear, specific title
2. A detailed description explaining the risk and its potential business impact
3. A category from: operational, compliance, security, financial
4. Which controls (by title) are related, and whether they adequately mitigate the risk

Focus on:
- Gaps in control coverage (areas with no controls)
- Controls that are not yet implemented or are in draft status
- Controls with weak effectiveness or no recent test results
- Common compliance and security risks that may not be covered

Return a JSON object with key "risks" containing an array of objects, each with:
"title", "description", "category", "related_controls" (array of control titles),
"gap_type" (one of: missing_control, weak_control, untested_control, coverage_gap)."""

SCORE_RISKS_PROMPT = """Score each of the following identified risks based on likelihood and impact.

Identified Risks:
{risks_json}

Organizational Context:
- Total controls: {total_controls}
- Implemented controls: {implemented_count}
- Draft/pending controls: {draft_count}

For each risk, assign:
1. likelihood: integer 1-5 (1=rare, 2=unlikely, 3=possible, 4=likely, 5=almost certain)
2. impact: integer 1-5 (1=negligible, 2=minor, 3=moderate, 4=major, 5=catastrophic)
3. risk_score: likelihood * impact (integer 1-25)
4. risk_level: based on risk_score (1-4=low, 5-9=medium, 10-15=high, 16-25=critical)
5. treatment_type: one of "mitigate", "accept", "transfer", "avoid"
6. treatment_recommendation: brief recommendation for risk treatment

Consider industry context, the maturity of existing controls, and the gap type when scoring.

Return a JSON object with key "scored_risks" containing an array of objects, each with:
"title", "description", "category", "likelihood", "impact", "risk_score", "risk_level",
"treatment_type", "treatment_recommendation"."""
