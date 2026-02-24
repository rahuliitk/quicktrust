"""Node functions for the audit preparation LangGraph."""
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.agents.common.llm import call_llm_json
from app.agents.audit_preparation.prompts import (
    SYSTEM_PROMPT,
    IDENTIFY_GAPS_PROMPT,
    GENERATE_WORKPAPERS_PROMPT,
)
from app.agents.audit_preparation.state import AuditPreparationState
from app.models.audit import Audit
from app.models.audit_finding import AuditFinding
from app.models.control import Control
from app.models.evidence import Evidence
from app.models.framework import Framework


async def load_audit_scope(
    state: AuditPreparationState, db: AsyncSession
) -> dict:
    """Load audit, framework, controls, and evidence from the database."""
    org_id = state["org_id"]
    audit_id = state["audit_id"]

    # Load audit with framework
    result = await db.execute(
        select(Audit).where(Audit.id == audit_id, Audit.org_id == org_id)
    )
    audit = result.scalar_one_or_none()
    if not audit:
        return {"error": f"Audit {audit_id} not found for organization {org_id}"}

    framework_id = str(audit.framework_id) if audit.framework_id else None

    # Load controls for org
    controls_result = await db.execute(
        select(Control)
        .options(selectinload(Control.evidence))
        .where(Control.org_id == org_id)
    )
    controls = controls_result.scalars().all()

    controls_data = []
    for c in controls:
        controls_data.append({
            "id": str(c.id),
            "title": c.title,
            "description": c.description or "",
            "status": c.status,
            "implementation_details": c.implementation_details or "",
            "effectiveness": c.effectiveness or "not_assessed",
            "last_test_date": str(c.last_test_date) if c.last_test_date else None,
            "last_test_result": c.last_test_result,
        })

    # Load all evidence for org
    evidence_result = await db.execute(
        select(Evidence).where(Evidence.org_id == org_id)
    )
    evidence_records = evidence_result.scalars().all()

    evidence_data = []
    for e in evidence_records:
        evidence_data.append({
            "id": str(e.id),
            "control_id": str(e.control_id),
            "title": e.title,
            "status": e.status,
            "collected_at": str(e.collected_at) if e.collected_at else None,
            "expires_at": str(e.expires_at) if e.expires_at else None,
            "collection_method": e.collection_method,
            "artifact_url": e.artifact_url,
        })

    return {
        "framework_id": framework_id,
        "controls": controls_data,
        "evidence": evidence_data,
    }


async def analyze_evidence_coverage(
    state: AuditPreparationState, db: AsyncSession
) -> dict:
    """Determine which controls have evidence and which do not."""
    controls = state["controls"]
    evidence = state["evidence"]

    # Group evidence by control
    evidence_by_control = {}
    for e in evidence:
        cid = e["control_id"]
        evidence_by_control.setdefault(cid, []).append(e)

    # Annotate controls with their evidence
    coverage = []
    for c in controls:
        ctrl_evidence = evidence_by_control.get(c["id"], [])
        coverage.append({
            **c,
            "evidence_items": ctrl_evidence,
            "evidence_count": len(ctrl_evidence),
            "has_evidence": len(ctrl_evidence) > 0,
            "has_valid_evidence": any(
                e["status"] in ("collected", "approved", "valid") for e in ctrl_evidence
            ),
        })

    return {"controls": coverage}


async def identify_gaps(
    state: AuditPreparationState, db: AsyncSession
) -> dict:
    """Use LLM to analyze gaps between requirements and evidence."""
    controls = state["controls"]
    framework_id = state.get("framework_id")

    # Get framework name
    framework_name = "General Compliance"
    if framework_id:
        result = await db.execute(
            select(Framework).where(Framework.id == framework_id)
        )
        fw = result.scalar_one_or_none()
        if fw:
            framework_name = fw.name

    prompt = IDENTIFY_GAPS_PROMPT.format(
        coverage_json=json.dumps(controls, indent=2),
        framework_name=framework_name,
    )

    try:
        result = await call_llm_json(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=8192,
        )
        gaps = result.get("gaps", [])
        return {"gaps": gaps}
    except Exception as e:
        # Fallback: generate gaps from controls without evidence
        fallback_gaps = []
        for c in controls:
            if not c.get("has_evidence"):
                fallback_gaps.append({
                    "control_id": c["id"],
                    "control_title": c["title"],
                    "gap_description": f"No evidence collected for control: {c['title']}",
                    "missing_evidence": "All evidence artifacts are missing",
                    "severity": "critical" if c["status"] == "implemented" else "major",
                    "recommended_action": "Collect and upload evidence demonstrating control operation",
                    "effort_estimate": "medium",
                })
            elif not c.get("has_valid_evidence"):
                fallback_gaps.append({
                    "control_id": c["id"],
                    "control_title": c["title"],
                    "gap_description": f"Evidence exists but is not in valid/approved state for: {c['title']}",
                    "missing_evidence": "Valid or approved evidence artifacts",
                    "severity": "major",
                    "recommended_action": "Review and approve pending evidence or collect fresh evidence",
                    "effort_estimate": "low",
                })
        return {"gaps": fallback_gaps, "error": f"LLM fallback used: {str(e)}"}


async def generate_workpapers(
    state: AuditPreparationState, db: AsyncSession
) -> dict:
    """Use LLM to generate audit workpaper summaries."""
    controls = state["controls"]
    gaps = state["gaps"]

    prompt = GENERATE_WORKPAPERS_PROMPT.format(
        coverage_json=json.dumps(controls, indent=2),
        gaps_json=json.dumps(gaps, indent=2),
    )

    try:
        result = await call_llm_json(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=8192,
        )
        workpapers = result.get("workpapers", [])
        return {"workpapers": workpapers}
    except Exception as e:
        # Fallback: generate basic workpapers
        fallback = []
        gap_control_ids = {g["control_id"] for g in gaps}
        for c in controls:
            has_gap = c["id"] in gap_control_ids
            fallback.append({
                "control_id": c["id"],
                "control_title": c["title"],
                "objective": f"Verify that {c['title']} is operating effectively",
                "control_activity": c.get("description", ""),
                "evidence_examined": [e["title"] for e in c.get("evidence_items", [])],
                "effectiveness_assessment": "Unable to fully assess" if has_gap else "Appears effective based on evidence",
                "exceptions_noted": ["Evidence gap identified"] if has_gap else [],
                "conclusion": "not_effective" if has_gap else "effective",
            })
        return {"workpapers": fallback, "error": f"LLM fallback used: {str(e)}"}


async def save_findings(
    state: AuditPreparationState, db: AsyncSession
) -> dict:
    """Update audit readiness_score and create AuditFinding records for gaps."""
    audit_id = state["audit_id"]
    org_id = state["org_id"]
    gaps = state["gaps"]
    controls = state["controls"]
    workpapers = state.get("workpapers", [])

    # Calculate readiness score
    total_controls = len(controls)
    if total_controls > 0:
        controls_with_valid_evidence = sum(
            1 for c in controls if c.get("has_valid_evidence")
        )
        readiness_score = round(
            (controls_with_valid_evidence / total_controls) * 100, 1
        )
    else:
        readiness_score = 0.0

    # Update audit readiness_score
    result = await db.execute(
        select(Audit).where(Audit.id == audit_id)
    )
    audit = result.scalar_one_or_none()
    if audit:
        audit.readiness_score = readiness_score

    # Create AuditFinding records for each gap
    findings_created = []
    for gap in gaps:
        finding = AuditFinding(
            audit_id=audit_id,
            org_id=org_id,
            control_id=gap.get("control_id"),
            title=f"Gap: {gap.get('control_title', 'Unknown')}",
            description=gap.get("gap_description", ""),
            severity=gap.get("severity", "medium"),
            status="open",
            remediation_plan=gap.get("recommended_action", ""),
        )
        db.add(finding)
        await db.flush()
        findings_created.append({
            "id": str(finding.id),
            "title": finding.title,
            "severity": finding.severity,
        })

    await db.commit()

    return {
        "readiness_assessment": {
            "readiness_score": readiness_score,
            "total_controls": total_controls,
            "gaps_found": len(gaps),
            "findings_created": len(findings_created),
            "workpapers_generated": len(workpapers),
        },
    }
