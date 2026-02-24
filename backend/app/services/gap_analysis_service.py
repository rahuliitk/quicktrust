"""Cross-framework gap analysis — identifies unmapped requirements and control gaps."""

from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.control import Control
from app.models.control_framework_mapping import ControlFrameworkMapping
from app.models.framework import Framework
from app.models.framework_domain import FrameworkDomain
from app.models.framework_requirement import FrameworkRequirement


async def get_gap_analysis(
    db: AsyncSession, org_id: UUID, framework_id: UUID
) -> dict:
    """Analyze gaps for a single framework: which requirements have no mapped controls."""
    # Get all requirements for this framework
    requirements = await db.execute(
        select(FrameworkRequirement)
        .join(FrameworkDomain)
        .where(FrameworkDomain.framework_id == framework_id)
        .order_by(FrameworkRequirement.sort_order)
    )
    all_reqs = list(requirements.scalars().all())

    # Get all mappings for this org and framework
    mappings = await db.execute(
        select(ControlFrameworkMapping)
        .join(Control, ControlFrameworkMapping.control_id == Control.id)
        .where(
            Control.org_id == org_id,
            ControlFrameworkMapping.framework_id == framework_id,
        )
    )
    mapped_req_ids = {m.requirement_id for m in mappings.scalars().all() if m.requirement_id}

    # Get controls mapped to this framework with their statuses
    controls_result = await db.execute(
        select(Control, ControlFrameworkMapping.requirement_id)
        .join(ControlFrameworkMapping, ControlFrameworkMapping.control_id == Control.id)
        .where(
            Control.org_id == org_id,
            ControlFrameworkMapping.framework_id == framework_id,
        )
    )
    control_rows = controls_result.all()

    # Build requirement-to-controls mapping
    req_controls: dict[str, list[dict]] = {}
    for ctrl, req_id in control_rows:
        if req_id:
            req_id_str = str(req_id)
            if req_id_str not in req_controls:
                req_controls[req_id_str] = []
            req_controls[req_id_str].append({
                "id": str(ctrl.id),
                "title": ctrl.title,
                "status": ctrl.status,
            })

    covered = []
    gaps = []
    partial = []

    for req in all_reqs:
        controls = req_controls.get(str(req.id), [])
        entry = {
            "requirement_id": str(req.id),
            "code": req.code,
            "title": req.title,
            "controls": controls,
        }
        if not controls:
            gaps.append(entry)
        elif all(c["status"] == "implemented" for c in controls):
            covered.append(entry)
        else:
            partial.append(entry)

    total_reqs = len(all_reqs)
    coverage_pct = round(len(covered) / total_reqs * 100, 1) if total_reqs else 0.0

    return {
        "framework_id": str(framework_id),
        "total_requirements": total_reqs,
        "covered_count": len(covered),
        "partial_count": len(partial),
        "gap_count": len(gaps),
        "coverage_percentage": coverage_pct,
        "covered": covered,
        "partial": partial,
        "gaps": gaps,
    }


async def get_cross_framework_matrix(
    db: AsyncSession, org_id: UUID
) -> dict:
    """Build a cross-framework control mapping matrix.

    Shows which controls map to multiple frameworks and identifies
    opportunities for deduplication.
    """
    # Get all active frameworks
    frameworks_result = await db.execute(
        select(Framework).where(Framework.is_active == True)  # noqa: E712
    )
    frameworks = list(frameworks_result.scalars().all())

    # Get all controls with their framework mappings
    controls_result = await db.execute(
        select(Control)
        .options(selectinload(Control.framework_mappings))
        .where(Control.org_id == org_id)
    )
    controls = list(controls_result.scalars().all())

    # Build matrix: for each control, list which frameworks it maps to
    matrix_rows = []
    multi_framework_count = 0

    for ctrl in controls:
        fw_ids = set()
        for mapping in (ctrl.framework_mappings or []):
            if mapping.framework_id:
                fw_ids.add(str(mapping.framework_id))

        if len(fw_ids) > 1:
            multi_framework_count += 1

        matrix_rows.append({
            "control_id": str(ctrl.id),
            "control_title": ctrl.title,
            "status": ctrl.status,
            "framework_ids": list(fw_ids),
            "framework_count": len(fw_ids),
        })

    # Per-framework summary
    framework_summaries = []
    for fw in frameworks:
        fw_id_str = str(fw.id)
        mapped_controls = [r for r in matrix_rows if fw_id_str in r["framework_ids"]]
        implemented = sum(1 for r in mapped_controls if r["status"] == "implemented")

        # Count total requirements
        req_count = (await db.execute(
            select(func.count())
            .select_from(FrameworkRequirement)
            .join(FrameworkDomain)
            .where(FrameworkDomain.framework_id == fw.id)
        )).scalar() or 0

        framework_summaries.append({
            "framework_id": fw_id_str,
            "framework_name": fw.name,
            "total_requirements": req_count,
            "mapped_controls": len(mapped_controls),
            "implemented_controls": implemented,
            "coverage_pct": round(
                implemented / req_count * 100, 1
            ) if req_count else 0.0,
        })

    return {
        "total_controls": len(controls),
        "multi_framework_controls": multi_framework_count,
        "deduplication_opportunity": multi_framework_count,
        "frameworks": framework_summaries,
        "matrix": sorted(
            matrix_rows, key=lambda r: r["framework_count"], reverse=True
        ),
    }
