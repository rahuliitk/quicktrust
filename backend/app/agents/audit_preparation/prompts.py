"""Prompt templates for the audit preparation agent."""

SYSTEM_PROMPT = """You are an expert audit preparation consultant with extensive experience in
SOC 2, ISO 27001, HIPAA, and other compliance frameworks. You help organizations prepare for
audits by identifying evidence gaps, assessing readiness, and generating comprehensive workpapers.
Your analysis is precise, thorough, and aligned with auditor expectations."""

IDENTIFY_GAPS_PROMPT = """Analyze the following controls and their associated evidence to identify
gaps that could cause audit findings.

Controls and Evidence Coverage:
{coverage_json}

Framework: {framework_name}

For each gap identified, provide:
1. The specific control that has insufficient evidence
2. What evidence is missing or inadequate
3. The severity of the gap: "critical" (will fail audit), "major" (likely finding), "minor" (observation)
4. Recommended action to close the gap before the audit
5. Estimated effort to remediate

Focus on:
- Controls with no evidence at all
- Controls with expired or stale evidence
- Controls where evidence does not fully demonstrate compliance
- Missing documentation or process artifacts

Return a JSON object with key "gaps" containing an array of objects, each with:
"control_id", "control_title", "gap_description", "missing_evidence",
"severity", "recommended_action", "effort_estimate"."""

GENERATE_WORKPAPERS_PROMPT = """Generate audit workpaper summaries for the following controls and evidence.
These workpapers will help the audit team quickly understand the control environment.

Controls with Evidence:
{coverage_json}

Identified Gaps:
{gaps_json}

For each control that has at least some evidence, generate a workpaper summary containing:
1. Control objective
2. Description of the control activity
3. Evidence examined (list what was reviewed)
4. Assessment of operating effectiveness
5. Any exceptions or gaps noted
6. Conclusion: "effective", "effective_with_exceptions", or "not_effective"

Return a JSON object with key "workpapers" containing an array of objects, each with:
"control_id", "control_title", "objective", "control_activity",
"evidence_examined" (array of strings), "effectiveness_assessment",
"exceptions_noted" (array of strings), "conclusion"."""
