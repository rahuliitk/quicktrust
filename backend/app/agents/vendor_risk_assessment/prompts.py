"""Prompt templates for the vendor risk assessment agent."""

SYSTEM_PROMPT = """You are an expert third-party risk management consultant specializing in vendor
due diligence and ongoing risk monitoring. You assess vendor risks based on data access levels,
contract terms, service criticality, and industry compliance requirements. Your assessments follow
established frameworks like NIST SP 800-161, ISO 27036, and SIG (Standardized Information Gathering)
questionnaire methodologies."""

ANALYZE_VENDOR_RISK_PROMPT = """Analyze the following vendor information and assess the risk they
pose to the organization.

Vendor Information:
- Name: {vendor_name}
- Category: {vendor_category}
- Website: {vendor_website}
- Status: {vendor_status}
- Contract Start: {contract_start}
- Contract End: {contract_end}
- Last Assessment: {last_assessment}
- Current Risk Tier: {current_risk_tier}
- Notes: {vendor_notes}
- Tags: {vendor_tags}

Analyze the vendor across these risk dimensions:
1. Data Access Risk: What level of access does this type of vendor typically have?
2. Business Continuity Risk: How critical is this vendor to operations?
3. Compliance Risk: What compliance obligations does this vendor relationship create?
4. Contractual Risk: Are there any concerns with contract terms or expiration?
5. Reputational Risk: What reputational exposure does this vendor create?

Return a JSON object with key "analysis" containing:
"data_access_risk" (object with "level" 1-5 and "rationale"),
"business_continuity_risk" (object with "level" 1-5 and "rationale"),
"compliance_risk" (object with "level" 1-5 and "rationale"),
"contractual_risk" (object with "level" 1-5 and "rationale"),
"reputational_risk" (object with "level" 1-5 and "rationale"),
"overall_summary" (string with overall risk assessment narrative)."""

SCORE_VENDOR_PROMPT = """Based on the following vendor risk analysis, calculate a final risk score
and assign a risk tier.

Vendor: {vendor_name}
Category: {vendor_category}

Risk Analysis:
{risk_analysis_json}

Calculate:
1. A weighted risk score from 0-100 where:
   - 0-25 = low risk
   - 26-50 = medium risk
   - 51-75 = high risk
   - 76-100 = critical risk
2. Assign a risk tier: "low", "medium", "high", or "critical"
3. Generate 3-5 specific, actionable recommendations to mitigate vendor risk
4. Suggest a reassessment timeline

Weighting guidance:
- Data access risk: 30%
- Business continuity risk: 25%
- Compliance risk: 25%
- Contractual risk: 10%
- Reputational risk: 10%

Return a JSON object with:
"risk_score" (integer 0-100),
"risk_tier" (string),
"recommendations" (array of objects with "title", "description", "priority"),
"reassessment_months" (integer, months until next assessment)."""
