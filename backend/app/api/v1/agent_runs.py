import asyncio
from uuid import UUID
from datetime import datetime, timezone

from fastapi import APIRouter, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser
from app.core.exceptions import NotFoundError
from app.models.agent_run import AgentRun
from app.schemas.agent_run import AgentRunResponse, AgentRunTrigger, AgentRunTriggerGeneric
from app.schemas.common import PaginatedResponse

router = APIRouter(prefix="/organizations/{org_id}/agents", tags=["agents"])


@router.post("/controls-generation/run", response_model=AgentRunResponse, status_code=201)
async def trigger_controls_generation(
    org_id: UUID, data: AgentRunTrigger, db: DB, current_user: ComplianceUser
):
    agent_run = AgentRun(
        org_id=org_id,
        agent_type="controls_generation",
        trigger="manual",
        status="pending",
        input_data={
            "framework_id": str(data.framework_id),
            "company_context": data.company_context or {},
        },
    )
    db.add(agent_run)
    await db.commit()
    await db.refresh(agent_run)

    # Launch the agent graph as a background task
    asyncio.create_task(_run_agent(str(agent_run.id), str(org_id)))

    return agent_run


async def _run_agent(agent_run_id: str, org_id: str):
    """Background task that runs the controls generation agent."""
    from app.core.database import async_session
    from app.agents.controls_generation.graph import run_controls_generation

    async with async_session() as db:
        run = await db.get(AgentRun, agent_run_id)
        if not run:
            return

        run.status = "running"
        run.started_at = datetime.now(timezone.utc)
        await db.commit()

        try:
            result = await run_controls_generation(
                db=db,
                org_id=org_id,
                agent_run_id=agent_run_id,
                framework_id=run.input_data["framework_id"],
                company_context=run.input_data.get("company_context", {}),
            )
            run.status = "completed"
            run.output_data = result
            run.completed_at = datetime.now(timezone.utc)
        except Exception as e:
            run.status = "failed"
            run.error_message = str(e)
            run.completed_at = datetime.now(timezone.utc)

        await db.commit()


@router.post("/policy-generation/run", response_model=AgentRunResponse, status_code=201)
async def trigger_policy_generation(
    org_id: UUID, data: AgentRunTrigger, db: DB, current_user: ComplianceUser
):
    agent_run = AgentRun(
        org_id=org_id,
        agent_type="policy_generation",
        trigger="manual",
        status="pending",
        input_data={
            "framework_id": str(data.framework_id),
            "company_context": data.company_context or {},
        },
    )
    db.add(agent_run)
    await db.commit()
    await db.refresh(agent_run)

    asyncio.create_task(_run_policy_agent(str(agent_run.id), str(org_id)))

    return agent_run


async def _run_policy_agent(agent_run_id: str, org_id: str):
    """Background task that runs the policy generation agent."""
    from app.core.database import async_session
    from app.agents.policy_generation.graph import run_policy_generation

    async with async_session() as db:
        run = await db.get(AgentRun, agent_run_id)
        if not run:
            return

        run.status = "running"
        run.started_at = datetime.now(timezone.utc)
        await db.commit()

        try:
            result = await run_policy_generation(
                db=db,
                org_id=org_id,
                agent_run_id=agent_run_id,
                framework_id=run.input_data["framework_id"],
                company_context=run.input_data.get("company_context", {}),
            )
            run.status = "completed"
            run.output_data = result
            run.completed_at = datetime.now(timezone.utc)
        except Exception as e:
            run.status = "failed"
            run.error_message = str(e)
            run.completed_at = datetime.now(timezone.utc)

        await db.commit()


@router.post("/evidence-generation/run", response_model=AgentRunResponse, status_code=201)
async def trigger_evidence_generation(
    org_id: UUID, data: AgentRunTrigger, db: DB, current_user: ComplianceUser
):
    agent_run = AgentRun(
        org_id=org_id,
        agent_type="evidence_generation",
        trigger="manual",
        status="pending",
        input_data={
            "framework_id": str(data.framework_id),
            "company_context": data.company_context or {},
        },
    )
    db.add(agent_run)
    await db.commit()
    await db.refresh(agent_run)

    asyncio.create_task(_run_evidence_agent(str(agent_run.id), str(org_id)))

    return agent_run


async def _run_evidence_agent(agent_run_id: str, org_id: str):
    """Background task that runs the evidence generation agent."""
    from app.core.database import async_session
    from app.agents.evidence_generation.graph import run_evidence_generation

    async with async_session() as db:
        run = await db.get(AgentRun, agent_run_id)
        if not run:
            return

        run.status = "running"
        run.started_at = datetime.now(timezone.utc)
        await db.commit()

        try:
            result = await run_evidence_generation(
                db=db,
                org_id=org_id,
                agent_run_id=agent_run_id,
                company_context=run.input_data.get("company_context", {}),
            )
            run.status = "completed"
            run.output_data = result
            run.completed_at = datetime.now(timezone.utc)
        except Exception as e:
            run.status = "failed"
            run.error_message = str(e)
            run.completed_at = datetime.now(timezone.utc)

        await db.commit()


@router.post("/risk-assessment/run", response_model=AgentRunResponse, status_code=201)
async def trigger_risk_assessment(
    org_id: UUID, data: AgentRunTriggerGeneric, db: DB, current_user: ComplianceUser
):
    agent_run = AgentRun(
        org_id=org_id,
        agent_type="risk_assessment",
        trigger="manual",
        status="pending",
        input_data={
            "framework_id": str(data.framework_id) if data.framework_id else None,
        },
    )
    db.add(agent_run)
    await db.commit()
    await db.refresh(agent_run)
    asyncio.create_task(_run_risk_assessment_agent(str(agent_run.id), str(org_id)))
    return agent_run


async def _run_risk_assessment_agent(agent_run_id: str, org_id: str):
    from app.core.database import async_session
    from app.agents.risk_assessment.graph import run_risk_assessment

    async with async_session() as db:
        run = await db.get(AgentRun, agent_run_id)
        if not run:
            return
        run.status = "running"
        run.started_at = datetime.now(timezone.utc)
        await db.commit()
        try:
            result = await run_risk_assessment(
                db=db, org_id=org_id, agent_run_id=agent_run_id,
                framework_id=run.input_data.get("framework_id"),
            )
            run.status = "completed"
            run.output_data = result
            run.completed_at = datetime.now(timezone.utc)
        except Exception as e:
            run.status = "failed"
            run.error_message = str(e)
            run.completed_at = datetime.now(timezone.utc)
        await db.commit()


@router.post("/remediation/run", response_model=AgentRunResponse, status_code=201)
async def trigger_remediation(
    org_id: UUID, data: AgentRunTriggerGeneric, db: DB, current_user: ComplianceUser
):
    agent_run = AgentRun(
        org_id=org_id,
        agent_type="remediation",
        trigger="manual",
        status="pending",
        input_data={},
    )
    db.add(agent_run)
    await db.commit()
    await db.refresh(agent_run)
    asyncio.create_task(_run_remediation_agent(str(agent_run.id), str(org_id)))
    return agent_run


async def _run_remediation_agent(agent_run_id: str, org_id: str):
    from app.core.database import async_session
    from app.agents.remediation.graph import run_remediation

    async with async_session() as db:
        run = await db.get(AgentRun, agent_run_id)
        if not run:
            return
        run.status = "running"
        run.started_at = datetime.now(timezone.utc)
        await db.commit()
        try:
            result = await run_remediation(db=db, org_id=org_id, agent_run_id=agent_run_id)
            run.status = "completed"
            run.output_data = result
            run.completed_at = datetime.now(timezone.utc)
        except Exception as e:
            run.status = "failed"
            run.error_message = str(e)
            run.completed_at = datetime.now(timezone.utc)
        await db.commit()


@router.post("/audit-preparation/run", response_model=AgentRunResponse, status_code=201)
async def trigger_audit_preparation(
    org_id: UUID, data: AgentRunTriggerGeneric, db: DB, current_user: ComplianceUser
):
    agent_run = AgentRun(
        org_id=org_id,
        agent_type="audit_preparation",
        trigger="manual",
        status="pending",
        input_data={
            "audit_id": str(data.audit_id) if data.audit_id else None,
        },
    )
    db.add(agent_run)
    await db.commit()
    await db.refresh(agent_run)
    asyncio.create_task(_run_audit_prep_agent(str(agent_run.id), str(org_id)))
    return agent_run


async def _run_audit_prep_agent(agent_run_id: str, org_id: str):
    from app.core.database import async_session
    from app.agents.audit_preparation.graph import run_audit_preparation

    async with async_session() as db:
        run = await db.get(AgentRun, agent_run_id)
        if not run:
            return
        run.status = "running"
        run.started_at = datetime.now(timezone.utc)
        await db.commit()
        try:
            result = await run_audit_preparation(
                db=db, org_id=org_id, agent_run_id=agent_run_id,
                audit_id=run.input_data.get("audit_id"),
            )
            run.status = "completed"
            run.output_data = result
            run.completed_at = datetime.now(timezone.utc)
        except Exception as e:
            run.status = "failed"
            run.error_message = str(e)
            run.completed_at = datetime.now(timezone.utc)
        await db.commit()


@router.post("/vendor-risk-assessment/run", response_model=AgentRunResponse, status_code=201)
async def trigger_vendor_risk_assessment(
    org_id: UUID, data: AgentRunTriggerGeneric, db: DB, current_user: ComplianceUser
):
    agent_run = AgentRun(
        org_id=org_id,
        agent_type="vendor_risk_assessment",
        trigger="manual",
        status="pending",
        input_data={
            "vendor_id": str(data.vendor_id) if data.vendor_id else None,
        },
    )
    db.add(agent_run)
    await db.commit()
    await db.refresh(agent_run)
    asyncio.create_task(_run_vendor_risk_agent(str(agent_run.id), str(org_id)))
    return agent_run


async def _run_vendor_risk_agent(agent_run_id: str, org_id: str):
    from app.core.database import async_session
    from app.agents.vendor_risk_assessment.graph import run_vendor_risk_assessment

    async with async_session() as db:
        run = await db.get(AgentRun, agent_run_id)
        if not run:
            return
        run.status = "running"
        run.started_at = datetime.now(timezone.utc)
        await db.commit()
        try:
            result = await run_vendor_risk_assessment(
                db=db, org_id=org_id, agent_run_id=agent_run_id,
                vendor_id=run.input_data.get("vendor_id"),
            )
            run.status = "completed"
            run.output_data = result
            run.completed_at = datetime.now(timezone.utc)
        except Exception as e:
            run.status = "failed"
            run.error_message = str(e)
            run.completed_at = datetime.now(timezone.utc)
        await db.commit()


@router.post("/pentest-orchestrator/run", response_model=AgentRunResponse, status_code=201)
async def trigger_pentest_orchestrator(
    org_id: UUID, data: AgentRunTriggerGeneric, db: DB, current_user: ComplianceUser
):
    agent_run = AgentRun(
        org_id=org_id,
        agent_type="pentest_orchestrator",
        trigger="manual",
        status="pending",
        input_data={},
    )
    db.add(agent_run)
    await db.commit()
    await db.refresh(agent_run)
    asyncio.create_task(_run_pentest_agent(str(agent_run.id), str(org_id)))
    return agent_run


async def _run_pentest_agent(agent_run_id: str, org_id: str):
    from app.core.database import async_session
    from app.agents.pentest_orchestrator.graph import run_pentest_orchestrator

    async with async_session() as db:
        run = await db.get(AgentRun, agent_run_id)
        if not run:
            return
        run.status = "running"
        run.started_at = datetime.now(timezone.utc)
        await db.commit()
        try:
            result = await run_pentest_orchestrator(db=db, org_id=org_id, agent_run_id=agent_run_id)
            run.status = "completed"
            run.output_data = result
            run.completed_at = datetime.now(timezone.utc)
        except Exception as e:
            run.status = "failed"
            run.error_message = str(e)
            run.completed_at = datetime.now(timezone.utc)
        await db.commit()


@router.post("/monitoring-daemon/run", response_model=AgentRunResponse, status_code=201)
async def trigger_monitoring_daemon(
    org_id: UUID, data: AgentRunTriggerGeneric, db: DB, current_user: ComplianceUser
):
    agent_run = AgentRun(
        org_id=org_id,
        agent_type="monitoring_daemon",
        trigger="manual",
        status="pending",
        input_data={},
    )
    db.add(agent_run)
    await db.commit()
    await db.refresh(agent_run)
    asyncio.create_task(_run_monitoring_daemon_agent(str(agent_run.id), str(org_id)))
    return agent_run


async def _run_monitoring_daemon_agent(agent_run_id: str, org_id: str):
    from app.core.database import async_session
    from app.agents.monitoring_daemon.graph import run_monitoring_daemon

    async with async_session() as db:
        run = await db.get(AgentRun, agent_run_id)
        if not run:
            return
        run.status = "running"
        run.started_at = datetime.now(timezone.utc)
        await db.commit()
        try:
            result = await run_monitoring_daemon(db=db, org_id=org_id, agent_run_id=agent_run_id)
            run.status = "completed"
            run.output_data = result
            run.completed_at = datetime.now(timezone.utc)
        except Exception as e:
            run.status = "failed"
            run.error_message = str(e)
            run.completed_at = datetime.now(timezone.utc)
        await db.commit()


@router.get("/runs", response_model=PaginatedResponse)
async def list_runs(
    org_id: UUID,
    db: DB,
    current_user: AnyInternalUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    count_q = select(func.count()).select_from(AgentRun).where(AgentRun.org_id == org_id)
    total = (await db.execute(count_q)).scalar() or 0

    q = (
        select(AgentRun)
        .where(AgentRun.org_id == org_id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(AgentRun.created_at.desc())
    )
    result = await db.execute(q)
    items = [AgentRunResponse.model_validate(r) for r in result.scalars().all()]

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/runs/{run_id}", response_model=AgentRunResponse)
async def get_run(org_id: UUID, run_id: UUID, db: DB, current_user: AnyInternalUser):
    result = await db.execute(
        select(AgentRun).where(AgentRun.id == run_id, AgentRun.org_id == org_id)
    )
    run = result.scalar_one_or_none()
    if not run:
        raise NotFoundError(f"Agent run {run_id} not found")
    return run
