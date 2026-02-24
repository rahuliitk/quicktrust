"""Node functions for the vendor risk assessment LangGraph."""
import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.common.llm import call_llm_json
from app.agents.vendor_risk_assessment.prompts import (
    SYSTEM_PROMPT,
    ANALYZE_VENDOR_RISK_PROMPT,
    SCORE_VENDOR_PROMPT,
)
from app.agents.vendor_risk_assessment.state import VendorRiskAssessmentState
from app.models.vendor import Vendor, VendorAssessment


async def load_vendor_info(
    state: VendorRiskAssessmentState, db: AsyncSession
) -> dict:
    """Load vendor information from the database."""
    org_id = state["org_id"]
    vendor_id = state["vendor_id"]

    result = await db.execute(
        select(Vendor).where(
            Vendor.id == vendor_id,
            Vendor.org_id == org_id,
        )
    )
    vendor = result.scalar_one_or_none()

    if not vendor:
        return {"error": f"Vendor {vendor_id} not found for organization {org_id}"}

    vendor_data = {
        "id": str(vendor.id),
        "name": vendor.name,
        "category": vendor.category or "uncategorized",
        "website": vendor.website or "",
        "status": vendor.status,
        "risk_tier": vendor.risk_tier,
        "contact_name": vendor.contact_name or "",
        "contact_email": vendor.contact_email or "",
        "contract_start_date": str(vendor.contract_start_date) if vendor.contract_start_date else None,
        "contract_end_date": str(vendor.contract_end_date) if vendor.contract_end_date else None,
        "last_assessment_date": str(vendor.last_assessment_date) if vendor.last_assessment_date else None,
        "assessment_score": vendor.assessment_score,
        "notes": vendor.notes or "",
        "tags": vendor.tags or [],
    }

    return {"vendor_data": vendor_data}


async def analyze_vendor_risk(
    state: VendorRiskAssessmentState, db: AsyncSession
) -> dict:
    """Use LLM to analyze vendor risk based on vendor data."""
    vendor = state["vendor_data"]

    prompt = ANALYZE_VENDOR_RISK_PROMPT.format(
        vendor_name=vendor["name"],
        vendor_category=vendor["category"],
        vendor_website=vendor["website"],
        vendor_status=vendor["status"],
        contract_start=vendor["contract_start_date"] or "Not specified",
        contract_end=vendor["contract_end_date"] or "Not specified",
        last_assessment=vendor["last_assessment_date"] or "Never assessed",
        current_risk_tier=vendor["risk_tier"],
        vendor_notes=vendor["notes"],
        vendor_tags=json.dumps(vendor["tags"]),
    )

    try:
        result = await call_llm_json(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=4096,
        )
        analysis = result.get("analysis", {})
        return {"risk_analysis": analysis}
    except Exception as e:
        # Fallback: generate basic risk analysis
        category_risk_map = {
            "cloud_infrastructure": 4,
            "saas": 3,
            "data_processor": 4,
            "consulting": 2,
            "hardware": 2,
            "uncategorized": 3,
        }
        base_level = category_risk_map.get(vendor["category"], 3)

        fallback = {
            "data_access_risk": {"level": base_level, "rationale": "Assessed based on vendor category"},
            "business_continuity_risk": {"level": base_level, "rationale": "Default assessment pending detailed review"},
            "compliance_risk": {"level": base_level, "rationale": "Default assessment pending detailed review"},
            "contractual_risk": {"level": 3 if not vendor["contract_end_date"] else 2, "rationale": "Contract status review needed"},
            "reputational_risk": {"level": 2, "rationale": "Default assessment pending detailed review"},
            "overall_summary": f"Automated baseline risk assessment for {vendor['name']}. Detailed review recommended.",
        }
        return {"risk_analysis": fallback, "error": f"LLM fallback used: {str(e)}"}


async def score_vendor(
    state: VendorRiskAssessmentState, db: AsyncSession
) -> dict:
    """Use LLM to calculate risk score and assign tier."""
    vendor = state["vendor_data"]
    analysis = state["risk_analysis"]

    prompt = SCORE_VENDOR_PROMPT.format(
        vendor_name=vendor["name"],
        vendor_category=vendor["category"],
        risk_analysis_json=json.dumps(analysis, indent=2),
    )

    try:
        result = await call_llm_json(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=4096,
        )
        risk_score = result.get("risk_score", 50)
        recommendations = result.get("recommendations", [])
        return {
            "risk_score": risk_score,
            "recommendations": recommendations,
            "assessment_criteria": result,
        }
    except Exception as e:
        # Fallback: calculate score from risk levels
        risk_dims = ["data_access_risk", "business_continuity_risk", "compliance_risk",
                      "contractual_risk", "reputational_risk"]
        weights = [0.30, 0.25, 0.25, 0.10, 0.10]
        total = 0
        for dim, weight in zip(risk_dims, weights):
            dim_data = analysis.get(dim, {})
            level = dim_data.get("level", 3) if isinstance(dim_data, dict) else 3
            total += (level / 5) * 100 * weight

        score = int(round(total))
        if score <= 25:
            tier = "low"
        elif score <= 50:
            tier = "medium"
        elif score <= 75:
            tier = "high"
        else:
            tier = "critical"

        fallback_recs = [
            {"title": "Conduct detailed vendor assessment", "description": "Perform a comprehensive vendor due diligence review.", "priority": "high"},
            {"title": "Review contractual safeguards", "description": "Ensure data protection clauses are in the vendor contract.", "priority": "medium"},
            {"title": "Establish monitoring cadence", "description": "Set up regular vendor performance and risk reviews.", "priority": "medium"},
        ]

        return {
            "risk_score": score,
            "recommendations": fallback_recs,
            "assessment_criteria": {"risk_score": score, "risk_tier": tier, "recommendations": fallback_recs},
            "error": f"LLM fallback used: {str(e)}",
        }


async def save_assessment(
    state: VendorRiskAssessmentState, db: AsyncSession
) -> dict:
    """Create VendorAssessment record and update vendor risk_tier."""
    vendor_data = state["vendor_data"]
    vendor_id = vendor_data["id"]
    org_id = state["org_id"]
    risk_score = state["risk_score"]
    criteria = state.get("assessment_criteria", {})

    # Determine risk tier from score
    if risk_score <= 25:
        risk_tier = "low"
    elif risk_score <= 50:
        risk_tier = "medium"
    elif risk_score <= 75:
        risk_tier = "high"
    else:
        risk_tier = "critical"

    now = datetime.now(timezone.utc)

    # Create assessment record
    assessment = VendorAssessment(
        vendor_id=vendor_id,
        org_id=org_id,
        assessment_date=now,
        score=risk_score,
        risk_tier_assigned=risk_tier,
        notes=json.dumps({
            "risk_analysis": state.get("risk_analysis", {}),
            "recommendations": state.get("recommendations", []),
        }),
        questionnaire_data=criteria,
    )
    db.add(assessment)

    # Update vendor risk tier and assessment date
    result = await db.execute(
        select(Vendor).where(Vendor.id == vendor_id)
    )
    vendor = result.scalar_one_or_none()
    if vendor:
        vendor.risk_tier = risk_tier
        vendor.assessment_score = risk_score
        vendor.last_assessment_date = now

    await db.commit()

    return {"saved": True}
