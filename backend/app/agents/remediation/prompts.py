"""Prompt templates for the remediation agent."""

SYSTEM_PROMPT = """You are an expert compliance remediation consultant with deep experience in
implementing security controls across diverse technology environments. You create practical,
step-by-step remediation plans that engineering and security teams can immediately act on.
Your plans consider effort level, team capacity, and business impact to help organizations
efficiently close compliance gaps."""

GENERATE_PLANS_PROMPT = """Analyze the following controls that are NOT fully implemented and generate
a detailed remediation plan for each one.

Failing Controls:
{controls_json}

For each control, generate a remediation plan that includes:
1. A clear summary of what needs to be done
2. Step-by-step implementation instructions (3-7 steps)
3. Effort estimate: one of "low" (< 1 day), "medium" (1-5 days), "high" (1-2 weeks), "very_high" (> 2 weeks)
4. Priority: one of "critical" (immediate security risk), "high" (compliance deadline), "medium" (best practice), "low" (nice to have)
5. Priority score: integer 1-100 (100 = highest priority)
6. Required resources or tools
7. Potential blockers or dependencies

Consider:
- Controls in "draft" status need full implementation
- Controls in "in_progress" status may need completion of remaining steps
- Controls with failed tests need investigation and fixes
- Automation opportunities that could accelerate remediation

Return a JSON object with key "plans" containing an array of objects, each with:
"control_id", "control_title", "summary", "steps" (array of strings),
"effort_estimate", "priority", "priority_score", "required_resources" (array of strings),
"blockers" (array of strings)."""
