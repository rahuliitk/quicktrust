"""Node functions for the risk assessment LangGraph."""
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.common.llm import call_llm_json
from app.agents.risk_assessment.prompts import (
    SYSTEM_PROMPT,
    IDENTIFY_RISKS_PROMPT,
    SCORE_RISKS_PROMPT,
)
from app.agents.risk_assessment.state import RiskAssessmentState
from app.models.control import Control
from app.models.risk import Risk


async def load_controls(
    state: RiskAssessmentState, db: AsyncSession
) -> dict:
    """Load all controls for the organization from DB."""
    org_id = state["org_id"]

    query = select(Control).where(Control.org_id == org_id)
    result = await db.execute(query)
    controls = result.scalars().all()

    if not controls:
        return {"error": f"No controls found for organization {org_id}"}

    controls_data = []
    for c in controls:
        controls_data.append({
            "id": str(c.id),
            "title": c.title,
            "description": c.description or "",
            "status": c.status,
            "effectiveness": c.effectiveness or "not_assessed",
            "automation_level": c.automation_level,
            "last_test_date": str(c.last_test_date) if c.last_test_date else None,
            "last_test_result": c.last_test_result,
            "implementation_details": c.implementation_details or "",
        })

    return {"controls": controls_data}


async def identify_risk_areas(
    state: RiskAssessmentState, db: AsyncSession
) -> dict:
    """Use LLM to identify potential risk areas based on control coverage."""
    controls = state["controls"]

    prompt = IDENTIFY_RISKS_PROMPT.format(
        controls_json=json.dumps(controls, indent=2),
    )

    try:
        result = await call_llm_json(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=8192,
        )
        risks = result.get("risks", [])
        return {"identified_risks": risks}
    except Exception as e:
        # Fallback: generate basic risks from control gaps
        fallback_risks = []
        statuses = {}
        for c in controls:
            statuses.setdefault(c["status"], []).append(c["title"])

        if statuses.get("draft"):
            fallback_risks.append({
                "title": "Unimplemented Security Controls",
                "description": f"{len(statuses['draft'])} controls remain in draft status, leaving potential security gaps.",
                "category": "security",
                "related_controls": statuses["draft"][:5],
                "gap_type": "weak_control",
            })
        if not any(c.get("last_test_date") for c in controls):
            fallback_risks.append({
                "title": "Untested Control Effectiveness",
                "description": "No controls have recent test results, making it impossible to verify effectiveness.",
                "category": "compliance",
                "related_controls": [c["title"] for c in controls[:5]],
                "gap_type": "untested_control",
            })

        return {"identified_risks": fallback_risks, "error": f"LLM fallback used: {str(e)}"}


async def score_risks(
    state: RiskAssessmentState, db: AsyncSession
) -> dict:
    """Use LLM to score each identified risk with likelihood and impact."""
    risks = state["identified_risks"]
    controls = state["controls"]

    if not risks:
        return {"scored_risks": []}

    implemented_count = sum(1 for c in controls if c["status"] == "implemented")
    draft_count = sum(1 for c in controls if c["status"] in ("draft", "pending"))

    prompt = SCORE_RISKS_PROMPT.format(
        risks_json=json.dumps(risks, indent=2),
        total_controls=len(controls),
        implemented_count=implemented_count,
        draft_count=draft_count,
    )

    try:
        result = await call_llm_json(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=8192,
        )
        scored = result.get("scored_risks", [])
        return {"scored_risks": scored}
    except Exception as e:
        # Fallback: assign default scores
        fallback = []
        for risk in risks:
            score = 9  # default medium
            fallback.append({
                "title": risk["title"],
                "description": risk["description"],
                "category": risk.get("category", "operational"),
                "likelihood": 3,
                "impact": 3,
                "risk_score": score,
                "risk_level": "medium",
                "treatment_type": "mitigate",
                "treatment_recommendation": "Review and implement controls to address this risk area.",
            })
        return {"scored_risks": fallback, "error": f"LLM fallback used: {str(e)}"}


async def save_to_db(
    state: RiskAssessmentState, db: AsyncSession
) -> dict:
    """Write scored risks to the Risk model in the database."""
    scored_risks = state["scored_risks"]
    org_id = state["org_id"]

    created_risks = []
    for risk_data in scored_risks:
        risk = Risk(
            org_id=org_id,
            title=risk_data.get("title", "Untitled Risk"),
            description=risk_data.get("description", ""),
            category=risk_data.get("category", "operational"),
            likelihood=risk_data.get("likelihood", 3),
            impact=risk_data.get("impact", 3),
            risk_score=risk_data.get("risk_score", 9),
            risk_level=risk_data.get("risk_level", "medium"),
            status="identified",
            treatment_type=risk_data.get("treatment_type", "mitigate"),
            treatment_plan=risk_data.get("treatment_recommendation", ""),
        )
        db.add(risk)
        await db.flush()

        created_risks.append({
            "id": str(risk.id),
            "title": risk.title,
            "category": risk.category,
            "risk_score": risk.risk_score,
            "risk_level": risk.risk_level,
        })

    await db.commit()

    return {
        "final_risks": created_risks,
        "risks_count": len(created_risks),
    }
