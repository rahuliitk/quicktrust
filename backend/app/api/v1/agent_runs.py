import asyncio
from uuid import UUID
from datetime import datetime, timezone

from fastapi import APIRouter, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import DB, CurrentUser
from app.core.exceptions import NotFoundError
from app.models.agent_run import AgentRun
from app.schemas.agent_run import AgentRunResponse, AgentRunTrigger
from app.schemas.common import PaginatedResponse

router = APIRouter(prefix="/organizations/{org_id}/agents", tags=["agents"])


@router.post("/controls-generation/run", response_model=AgentRunResponse, status_code=201)
async def trigger_controls_generation(
    org_id: UUID, data: AgentRunTrigger, db: DB, current_user: CurrentUser
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


@router.get("/runs", response_model=PaginatedResponse)
async def list_runs(
    org_id: UUID,
    db: DB,
    current_user: CurrentUser,
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
async def get_run(org_id: UUID, run_id: UUID, db: DB, current_user: CurrentUser):
    result = await db.execute(
        select(AgentRun).where(AgentRun.id == run_id, AgentRun.org_id == org_id)
    )
    run = result.scalar_one_or_none()
    if not run:
        raise NotFoundError(f"Agent run {run_id} not found")
    return run
