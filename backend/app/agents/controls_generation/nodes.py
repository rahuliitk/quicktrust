"""Node functions for the controls generation LangGraph."""
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.agents.common.llm import call_llm_json
from app.agents.controls_generation.prompts import (
    SYSTEM_PROMPT,
    CUSTOMIZE_CONTROLS_PROMPT,
    SUGGEST_OWNERS_PROMPT,
)
from app.agents.controls_generation.state import ControlsGenerationState
from app.models.control import Control
from app.models.control_framework_mapping import ControlFrameworkMapping
from app.models.control_template import ControlTemplate
from app.models.control_template_framework_mapping import ControlTemplateFrameworkMapping
from app.models.framework import Framework
from app.models.framework_domain import FrameworkDomain
from app.models.framework_requirement import FrameworkRequirement


async def load_framework_requirements(
    state: ControlsGenerationState, db: AsyncSession
) -> dict:
    """Load all requirements for the selected framework. No LLM needed."""
    framework_id = state["framework_id"]
    result = await db.execute(
        select(Framework)
        .options(
            selectinload(Framework.domains)
            .selectinload(FrameworkDomain.requirements)
        )
        .where(Framework.id == framework_id)
    )
    framework = result.scalar_one_or_none()
    if not framework:
        return {"error": f"Framework {framework_id} not found"}

    requirements = []
    for domain in framework.domains:
        for req in domain.requirements:
            requirements.append({
                "id": str(req.id),
                "code": req.code,
                "title": req.title,
                "description": req.description,
                "domain_code": domain.code,
                "domain_name": domain.name,
            })

    return {"requirements": requirements}


async def match_templates_to_requirements(
    state: ControlsGenerationState, db: AsyncSession
) -> dict:
    """Match control templates to framework requirements. DB query + scoring."""
    framework_id = state["framework_id"]
    requirements = state["requirements"]
    req_codes = {r["code"] for r in requirements}

    # Get all templates with their framework mappings
    result = await db.execute(
        select(ControlTemplate)
        .options(selectinload(ControlTemplate.framework_mappings))
    )
    all_templates = result.scalars().all()

    matched = []
    for template in all_templates:
        template_req_codes = {
            m.requirement_code
            for m in template.framework_mappings
            if str(m.framework_id) == framework_id
        }
        overlap = template_req_codes & req_codes
        if overlap:
            matched.append({
                "template_code": template.template_code,
                "title": template.title,
                "domain": template.domain,
                "description": template.description,
                "implementation_guidance": template.implementation_guidance,
                "test_procedure": template.test_procedure,
                "automation_level": template.automation_level,
                "variables": template.variables or {},
                "requirement_codes": list(overlap),
                "match_score": len(overlap),
            })

    matched.sort(key=lambda x: x["match_score"], reverse=True)
    return {"matched_templates": matched, "templates": matched}


async def customize_controls(
    state: ControlsGenerationState, db: AsyncSession
) -> dict:
    """Use LLM to customize control templates for the company context."""
    context = state.get("company_context", {})
    templates = state["matched_templates"]

    if not templates:
        return {"customized_controls": []}

    prompt = CUSTOMIZE_CONTROLS_PROMPT.format(
        company_name=context.get("name", "the company"),
        industry=context.get("industry", "Technology"),
        company_size=context.get("company_size", "50-200"),
        cloud_providers=", ".join(context.get("cloud_providers", ["AWS"])),
        tech_stack=", ".join(context.get("tech_stack", [])),
        templates_json=json.dumps(templates, indent=2),
    )

    try:
        result = await call_llm_json(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=8192,
        )
        controls = result.get("controls", [])
        return {"customized_controls": controls}
    except Exception as e:
        # Fallback: use templates as-is with basic substitution
        fallback = []
        cloud = context.get("cloud_providers", ["AWS"])[0] if context.get("cloud_providers") else "AWS"
        for t in templates:
            control = {
                "template_code": t["template_code"],
                "title": t["title"],
                "description": t["description"],
                "implementation_details": (t.get("implementation_guidance") or "").replace("{cloud_provider}", cloud),
                "automation_level": t["automation_level"],
                "test_procedure": t.get("test_procedure", ""),
                "requirement_codes": t["requirement_codes"],
                "domain": t["domain"],
            }
            fallback.append(control)
        return {"customized_controls": fallback, "error": f"LLM fallback used: {str(e)}"}


async def deduplicate_controls(
    state: ControlsGenerationState, db: AsyncSession
) -> dict:
    """Pure logic: merge controls that satisfy multiple requirements."""
    controls = state["customized_controls"]
    seen_codes = {}
    deduped = []

    for control in controls:
        code = control.get("template_code", "")
        if code in seen_codes:
            # Merge requirement codes
            existing = seen_codes[code]
            existing_reqs = set(existing.get("requirement_codes", []))
            new_reqs = set(control.get("requirement_codes", []))
            existing["requirement_codes"] = list(existing_reqs | new_reqs)
        else:
            seen_codes[code] = control
            deduped.append(control)

    return {"deduplicated_controls": deduped}


async def suggest_owners(
    state: ControlsGenerationState, db: AsyncSession
) -> dict:
    """Use LLM to suggest department owners for each control."""
    controls = state["deduplicated_controls"]
    context = state.get("company_context", {})

    departments = context.get("departments", [
        "Engineering", "IT", "Security", "HR", "Legal", "Finance", "Operations"
    ])

    try:
        prompt = SUGGEST_OWNERS_PROMPT.format(
            departments=", ".join(departments),
            controls_json=json.dumps(
                [{"template_code": c["template_code"], "title": c["title"], "domain": c["domain"]}
                 for c in controls],
                indent=2,
            ),
        )

        result = await call_llm_json(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )

        assignments = {
            a["template_code"]: a["suggested_owner_department"]
            for a in result.get("assignments", [])
        }

        for control in controls:
            control["suggested_owner_department"] = assignments.get(
                control["template_code"], "Engineering"
            )
    except Exception:
        # Fallback: assign based on domain
        domain_map = {
            "Access Control": "IT",
            "Network Security": "Engineering",
            "Data Protection": "Engineering",
            "Change Management": "Engineering",
            "Logging & Monitoring": "Security",
            "Incident Response": "Security",
            "Endpoint Security": "IT",
            "HR Security": "HR",
        }
        for control in controls:
            control["suggested_owner_department"] = domain_map.get(
                control.get("domain", ""), "Engineering"
            )

    return {"controls_with_owners": controls}


async def finalize_output(
    state: ControlsGenerationState, db: AsyncSession
) -> dict:
    """Write controls to DB as status='draft' and update agent_run."""
    controls = state["controls_with_owners"]
    org_id = state["org_id"]
    agent_run_id = state["agent_run_id"]
    framework_id = state["framework_id"]

    created_controls = []
    for ctrl_data in controls:
        control = Control(
            org_id=org_id,
            title=ctrl_data.get("title", "Untitled Control"),
            description=ctrl_data.get("description", ""),
            implementation_details=ctrl_data.get("implementation_details", ""),
            status="draft",
            automation_level=ctrl_data.get("automation_level", "manual"),
            test_procedure=ctrl_data.get("test_procedure", ""),
            agent_run_id=agent_run_id,
        )
        db.add(control)
        await db.flush()

        # Create framework mapping
        for req_code in ctrl_data.get("requirement_codes", []):
            req_result = await db.execute(
                select(FrameworkRequirement).where(FrameworkRequirement.code == req_code)
            )
            req = req_result.scalar_one_or_none()
            if req:
                mapping = ControlFrameworkMapping(
                    control_id=control.id,
                    framework_id=framework_id,
                    requirement_id=req.id,
                )
                db.add(mapping)

        created_controls.append({
            "id": str(control.id),
            "title": control.title,
            "status": control.status,
            "domain": ctrl_data.get("domain", ""),
            "suggested_owner": ctrl_data.get("suggested_owner_department", ""),
        })

    await db.commit()

    return {
        "final_controls": created_controls,
        "controls_count": len(created_controls),
    }
