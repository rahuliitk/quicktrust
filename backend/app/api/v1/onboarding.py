import asyncio
from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import DB, CurrentUser
from app.schemas.onboarding import OnboardingWizardInput, OnboardingSessionResponse
from app.services import onboarding_service

router = APIRouter(
    prefix="/organizations/{org_id}/onboarding",
    tags=["onboarding"],
)


@router.post("/start", response_model=OnboardingSessionResponse, status_code=201)
async def start_onboarding(
    org_id: UUID, data: OnboardingWizardInput, db: DB, current_user: CurrentUser
):
    session = await onboarding_service.start_onboarding(db, org_id, data)

    # Launch the pipeline as a background task
    asyncio.create_task(_run_pipeline(str(session.id), str(org_id)))

    return session


async def _run_pipeline(session_id: str, org_id: str):
    """Background task that runs the onboarding pipeline."""
    from app.core.database import async_session

    async with async_session() as db:
        await onboarding_service.run_onboarding_pipeline(db, session_id, org_id)


@router.get("/status/{session_id}", response_model=OnboardingSessionResponse)
async def get_onboarding_status(
    org_id: UUID, session_id: UUID, db: DB, current_user: CurrentUser
):
    return await onboarding_service.get_session(db, org_id, session_id)


@router.get("/latest", response_model=OnboardingSessionResponse | None)
async def get_latest_onboarding(org_id: UUID, db: DB, current_user: CurrentUser):
    return await onboarding_service.get_latest_session(db, org_id)
