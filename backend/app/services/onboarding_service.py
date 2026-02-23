"""Onboarding orchestrator — runs all generation agents in sequence."""
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.agent_run import AgentRun
from app.models.onboarding_session import OnboardingSession
from app.models.organization import Organization
from app.schemas.onboarding import OnboardingWizardInput


async def start_onboarding(
    db: AsyncSession, org_id: UUID, data: OnboardingWizardInput
) -> OnboardingSession:
    """Create onboarding session and return it (actual work runs in background)."""
    session = OnboardingSession(
        org_id=org_id,
        status="in_progress",
        input_data=data.model_dump(mode="json"),
        progress={"current_step": "initializing", "steps_completed": []},
        results={},
        agent_run_ids={},
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def run_onboarding_pipeline(db: AsyncSession, session_id: str, org_id: str):
    """Execute the full onboarding pipeline. Called as a background task."""
    from app.agents.controls_generation.graph import run_controls_generation
    from app.agents.policy_generation.graph import run_policy_generation
    from app.agents.evidence_generation.graph import run_evidence_generation

    session = await db.get(OnboardingSession, session_id)
    if not session:
        return

    input_data = session.input_data or {}
    company_context = {
        "company_name": input_data.get("company_name", "Organization"),
        "industry": input_data.get("industry", "Technology"),
        "company_size": input_data.get("company_size", ""),
        "cloud_providers": input_data.get("cloud_providers", []),
        "tech_stack": input_data.get("tech_stack", []),
        "departments": input_data.get("departments", []),
    }
    framework_ids = input_data.get("target_framework_ids", [])
    agent_run_ids = {}
    results = {}

    try:
        # Step 1: Update organization with company details
        _update_progress(session, "updating_organization")
        org = await db.get(Organization, org_id)
        if org:
            org.industry = input_data.get("industry")
            org.company_size = input_data.get("company_size")
            org.cloud_providers = input_data.get("cloud_providers")
            org.tech_stack = input_data.get("tech_stack")
            await db.commit()
        session.progress["steps_completed"].append("organization_updated")
        await db.commit()

        # Step 2: Generate controls for each framework
        total_controls = 0
        for fw_id in framework_ids:
            _update_progress(session, f"generating_controls_{fw_id}")
            agent_run = AgentRun(
                org_id=org_id,
                agent_type="controls_generation",
                trigger="onboarding",
                status="running",
                started_at=datetime.now(timezone.utc),
                input_data={"framework_id": str(fw_id), "company_context": company_context},
            )
            db.add(agent_run)
            await db.commit()
            await db.refresh(agent_run)

            try:
                result = await run_controls_generation(
                    db=db,
                    org_id=org_id,
                    agent_run_id=str(agent_run.id),
                    framework_id=str(fw_id),
                    company_context=company_context,
                )
                agent_run.status = "completed"
                agent_run.output_data = result
                agent_run.completed_at = datetime.now(timezone.utc)
                total_controls += result.get("controls_count", 0)
            except Exception as e:
                agent_run.status = "failed"
                agent_run.error_message = str(e)
                agent_run.completed_at = datetime.now(timezone.utc)

            await db.commit()
            agent_run_ids[f"controls_{fw_id}"] = str(agent_run.id)

        session.progress["steps_completed"].append("controls_generated")
        results["controls_count"] = total_controls
        await db.commit()

        # Step 3: Generate policies (once for all controls)
        _update_progress(session, "generating_policies")
        policy_run = AgentRun(
            org_id=org_id,
            agent_type="policy_generation",
            trigger="onboarding",
            status="running",
            started_at=datetime.now(timezone.utc),
            input_data={
                "framework_id": str(framework_ids[0]) if framework_ids else "",
                "company_context": company_context,
            },
        )
        db.add(policy_run)
        await db.commit()
        await db.refresh(policy_run)

        try:
            policy_result = await run_policy_generation(
                db=db,
                org_id=org_id,
                agent_run_id=str(policy_run.id),
                framework_id=str(framework_ids[0]) if framework_ids else "",
                company_context=company_context,
            )
            policy_run.status = "completed"
            policy_run.output_data = policy_result
            policy_run.completed_at = datetime.now(timezone.utc)
            results["policies_count"] = policy_result.get("policies_count", 0)
        except Exception as e:
            policy_run.status = "failed"
            policy_run.error_message = str(e)
            policy_run.completed_at = datetime.now(timezone.utc)
            results["policies_count"] = 0

        await db.commit()
        agent_run_ids["policies"] = str(policy_run.id)
        session.progress["steps_completed"].append("policies_generated")
        await db.commit()

        # Step 4: Generate evidence
        _update_progress(session, "generating_evidence")
        evidence_run = AgentRun(
            org_id=org_id,
            agent_type="evidence_generation",
            trigger="onboarding",
            status="running",
            started_at=datetime.now(timezone.utc),
            input_data={"company_context": company_context},
        )
        db.add(evidence_run)
        await db.commit()
        await db.refresh(evidence_run)

        try:
            evidence_result = await run_evidence_generation(
                db=db,
                org_id=org_id,
                agent_run_id=str(evidence_run.id),
                company_context=company_context,
            )
            evidence_run.status = "completed"
            evidence_run.output_data = evidence_result
            evidence_run.completed_at = datetime.now(timezone.utc)
            results["evidence_count"] = evidence_result.get("evidence_count", 0)
        except Exception as e:
            evidence_run.status = "failed"
            evidence_run.error_message = str(e)
            evidence_run.completed_at = datetime.now(timezone.utc)
            results["evidence_count"] = 0

        await db.commit()
        agent_run_ids["evidence"] = str(evidence_run.id)
        session.progress["steps_completed"].append("evidence_generated")

        # Finalize
        session.status = "completed"
        session.results = results
        session.agent_run_ids = agent_run_ids
        session.progress["current_step"] = "completed"

    except Exception as e:
        session.status = "failed"
        session.progress["current_step"] = "failed"
        session.progress["error"] = str(e)

    await db.commit()


def _update_progress(session: OnboardingSession, step: str):
    session.progress["current_step"] = step


async def get_session(db: AsyncSession, org_id: UUID, session_id: UUID) -> OnboardingSession:
    result = await db.execute(
        select(OnboardingSession).where(
            OnboardingSession.id == session_id,
            OnboardingSession.org_id == org_id,
        )
    )
    session = result.scalar_one_or_none()
    if not session:
        raise NotFoundError(f"Onboarding session {session_id} not found")
    return session


async def get_latest_session(db: AsyncSession, org_id: UUID) -> OnboardingSession | None:
    result = await db.execute(
        select(OnboardingSession).where(
            OnboardingSession.org_id == org_id
        ).order_by(OnboardingSession.created_at.desc()).limit(1)
    )
    return result.scalar_one_or_none()
