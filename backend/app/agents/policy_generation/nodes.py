"""Policy generation agent nodes — sequential pipeline steps."""
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.agents.common.llm import call_llm_json
from app.agents.policy_generation.prompts import SYSTEM_PROMPT, GENERATE_POLICY_PROMPT
from app.agents.policy_generation.state import PolicyGenerationState
from app.models.control import Control
from app.models.policy import Policy
from app.models.policy_template import PolicyTemplate


async def identify_required_policies(
    state: PolicyGenerationState, db: AsyncSession
) -> dict:
    """Query approved controls, map control domains to policy templates."""
    org_id = state["org_id"]

    # Get all controls for this org (any status — policies cover all)
    result = await db.execute(
        select(Control).where(Control.org_id == org_id)
    )
    controls = list(result.scalars().all())

    if not controls:
        return {"controls": [], "policies_needed": []}

    # Group controls by rough domain categories
    domain_keywords = {
        "Information Security": ["security", "access", "authentication", "encryption", "mfa"],
        "Acceptable Use": ["acceptable", "usage", "workstation", "endpoint"],
        "Access Control": ["access", "provisioning", "rbac", "privilege", "mfa", "authentication"],
        "Data Classification": ["data", "classification", "encryption", "retention", "backup"],
        "Incident Response": ["incident", "response", "security event", "breach"],
        "Change Management": ["change", "deployment", "release", "version", "ci/cd"],
        "Vendor Management": ["vendor", "third-party", "supplier", "partner"],
        "Password & Authentication": ["password", "mfa", "authentication", "credential"],
        "Remote Work": ["remote", "vpn", "byod", "work from home"],
        "Risk Management": ["risk", "assessment", "mitigation", "vulnerability"],
    }

    policies_needed = []
    control_dicts = []
    for c in controls:
        title_desc = f"{c.title} {c.description or ''}".lower()
        control_dicts.append({
            "id": str(c.id),
            "title": c.title,
            "description": c.description or "",
            "status": c.status,
        })
        for policy_name, keywords in domain_keywords.items():
            if any(kw in title_desc for kw in keywords):
                if policy_name not in [p["name"] for p in policies_needed]:
                    policies_needed.append({
                        "name": policy_name,
                        "control_ids": [str(c.id)],
                    })
                else:
                    existing = next(p for p in policies_needed if p["name"] == policy_name)
                    existing["control_ids"].append(str(c.id))

    return {"controls": control_dicts, "policies_needed": policies_needed}


async def match_policy_templates(
    state: PolicyGenerationState, db: AsyncSession
) -> dict:
    """Score and select policy templates from the library."""
    policies_needed = state.get("policies_needed", [])

    result = await db.execute(select(PolicyTemplate))
    all_templates = list(result.scalars().all())

    if not all_templates:
        return {"matched_templates": []}

    matched = []
    needed_names = {p["name"].lower() for p in policies_needed}

    for template in all_templates:
        title_lower = template.title.lower()
        # Match by title similarity to needed policy names
        score = 0
        matched_policy_name = None
        for name in needed_names:
            name_words = name.split()
            matches = sum(1 for w in name_words if w in title_lower)
            if matches > score:
                score = matches
                matched_policy_name = name

        # Also match all templates if we have controls (comprehensive policy set)
        if score > 0 or policies_needed:
            control_ids = []
            if matched_policy_name:
                for p in policies_needed:
                    if p["name"].lower() == matched_policy_name:
                        control_ids = p["control_ids"]
                        break

            matched.append({
                "template_id": str(template.id),
                "template_code": template.template_code,
                "title": template.title,
                "category": template.category,
                "description": template.description,
                "sections": template.sections or [],
                "variables": template.variables or [],
                "content_template": template.content_template or "",
                "review_frequency": template.review_frequency,
                "required_by_frameworks": template.required_by_frameworks or [],
                "match_score": score,
                "control_ids": control_ids,
            })

    matched.sort(key=lambda x: x["match_score"], reverse=True)
    return {"matched_templates": matched}


async def generate_policy_content(
    state: PolicyGenerationState, db: AsyncSession
) -> dict:
    """LLM generates policy Markdown content per template."""
    context = state.get("company_context", {})
    templates = state.get("matched_templates", [])
    controls = state.get("controls", [])

    if not templates:
        return {"generated_policies": []}

    company_name = context.get("name", "the company")
    industry = context.get("industry", "Technology")
    company_size = context.get("company_size", "50-200")
    cloud_providers = ", ".join(context.get("cloud_providers", ["AWS"]))
    tech_stack = ", ".join(context.get("tech_stack", []))

    generated = []
    for template in templates:
        # Find related controls for this template
        related_control_ids = set(template.get("control_ids", []))
        related_controls = [
            f"- {c['title']}: {c['description'][:100]}"
            for c in controls
            if c["id"] in related_control_ids
        ]
        if not related_controls:
            related_controls = [f"- {c['title']}" for c in controls[:5]]

        prompt = GENERATE_POLICY_PROMPT.format(
            company_name=company_name,
            industry=industry,
            company_size=company_size,
            cloud_providers=cloud_providers,
            tech_stack=tech_stack,
            template_title=template["title"],
            template_category=template["category"],
            template_sections=json.dumps(template["sections"]),
            template_variables=json.dumps(template["variables"]),
            related_controls="\n".join(related_controls),
            content_template=template.get("content_template", ""),
        )

        try:
            result = await call_llm_json(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=8192,
            )
            generated.append({
                "template_code": template["template_code"],
                "title": result.get("title", template["title"]),
                "content": result.get("content", ""),
                "category": template["category"],
                "framework_ids": [state.get("framework_id", "")],
                "control_ids": template.get("control_ids", []),
                "sections": result.get("sections", template["sections"]),
            })
        except Exception:
            # Fallback: basic variable substitution on content_template
            content = template.get("content_template", f"# {template['title']}\n\nPolicy document pending generation.")
            content = content.replace("{company_name}", company_name)
            content = content.replace("{industry}", industry)
            content = content.replace("{cloud_providers}", cloud_providers)
            content = content.replace("{tech_stack}", tech_stack)
            content = content.replace("{company_size}", company_size)

            generated.append({
                "template_code": template["template_code"],
                "title": template["title"],
                "content": content,
                "category": template["category"],
                "framework_ids": [state.get("framework_id", "")],
                "control_ids": template.get("control_ids", []),
                "sections": template["sections"],
            })

    return {"generated_policies": generated}


async def finalize_policies(
    state: PolicyGenerationState, db: AsyncSession
) -> dict:
    """Persist policies to DB as status='draft', link to agent_run."""
    generated = state.get("generated_policies", [])
    org_id = state["org_id"]
    agent_run_id = state["agent_run_id"]

    created = []
    for policy_data in generated:
        policy = Policy(
            org_id=org_id,
            title=policy_data.get("title", "Untitled Policy"),
            content=policy_data.get("content", ""),
            status="draft",
            version="1.0",
            framework_ids=policy_data.get("framework_ids", []),
            control_ids=policy_data.get("control_ids", []),
            agent_run_id=agent_run_id,
        )
        db.add(policy)
        await db.flush()

        created.append({
            "id": str(policy.id),
            "title": policy.title,
            "status": policy.status,
            "category": policy_data.get("category", ""),
        })

    await db.commit()

    return {
        "final_policies": created,
        "policies_count": len(created),
    }
