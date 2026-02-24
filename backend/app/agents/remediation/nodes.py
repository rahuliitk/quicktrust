"""Node functions for the remediation LangGraph."""
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.common.llm import call_llm_json
from app.agents.remediation.prompts import (
    SYSTEM_PROMPT,
    GENERATE_PLANS_PROMPT,
)
from app.agents.remediation.state import RemediationState
from app.models.control import Control


async def load_failing_controls(
    state: RemediationState, db: AsyncSession
) -> dict:
    """Load controls that are not fully implemented from the database."""
    org_id = state["org_id"]

    query = select(Control).where(
        Control.org_id == org_id,
        Control.status != "implemented",
    )
    result = await db.execute(query)
    controls = result.scalars().all()

    if not controls:
        return {"error": f"No failing controls found for organization {org_id}"}

    controls_data = []
    for c in controls:
        controls_data.append({
            "id": str(c.id),
            "title": c.title,
            "description": c.description or "",
            "status": c.status,
            "implementation_details": c.implementation_details or "",
            "automation_level": c.automation_level,
            "last_test_date": str(c.last_test_date) if c.last_test_date else None,
            "last_test_result": c.last_test_result,
        })

    return {"failing_controls": controls_data}


async def generate_remediation_plans(
    state: RemediationState, db: AsyncSession
) -> dict:
    """Use LLM to generate step-by-step remediation plans for failing controls."""
    controls = state["failing_controls"]

    if not controls:
        return {"remediation_plans": []}

    prompt = GENERATE_PLANS_PROMPT.format(
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
        plans = result.get("plans", [])
        return {"remediation_plans": plans}
    except Exception as e:
        # Fallback: generate basic remediation plans
        fallback = []
        for c in controls:
            priority_score = 80 if c["status"] == "draft" else 60
            fallback.append({
                "control_id": c["id"],
                "control_title": c["title"],
                "summary": f"Implement control: {c['title']}",
                "steps": [
                    "Review the control requirements and description",
                    "Assign an owner to the control",
                    "Develop implementation plan with timeline",
                    "Implement the control according to specifications",
                    "Test the control effectiveness",
                    "Document evidence of implementation",
                ],
                "effort_estimate": "medium",
                "priority": "high" if c["status"] == "draft" else "medium",
                "priority_score": priority_score,
                "required_resources": ["Control owner", "Engineering team"],
                "blockers": [],
            })
        return {"remediation_plans": fallback, "error": f"LLM fallback used: {str(e)}"}


async def prioritize(
    state: RemediationState, db: AsyncSession
) -> dict:
    """Sort remediation plans by priority score (critical first)."""
    plans = state["remediation_plans"]

    prioritized = sorted(
        plans,
        key=lambda p: p.get("priority_score", 50),
        reverse=True,
    )

    return {"prioritized_plans": prioritized}


async def save_to_db(
    state: RemediationState, db: AsyncSession
) -> dict:
    """Update controls with remediation guidance in implementation_details."""
    plans = state["prioritized_plans"]
    saved = 0

    for plan in plans:
        control_id = plan.get("control_id")
        if not control_id:
            continue

        result = await db.execute(
            select(Control).where(Control.id == control_id)
        )
        control = result.scalar_one_or_none()
        if not control:
            continue

        # Build remediation text to append to implementation_details
        steps_text = "\n".join(f"  {i+1}. {step}" for i, step in enumerate(plan.get("steps", [])))
        remediation_text = (
            f"\n\n--- Remediation Plan (Priority: {plan.get('priority', 'medium')}) ---\n"
            f"Summary: {plan.get('summary', '')}\n"
            f"Effort: {plan.get('effort_estimate', 'medium')}\n"
            f"Steps:\n{steps_text}\n"
            f"Resources: {', '.join(plan.get('required_resources', []))}\n"
        )

        existing = control.implementation_details or ""
        control.implementation_details = existing + remediation_text
        saved += 1

    await db.commit()

    return {"saved_count": saved}
