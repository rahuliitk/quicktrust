from fastapi import APIRouter

from app.api.v1 import (
    auth,
    organizations,
    users,
    frameworks,
    control_templates,
    evidence_templates,
    controls,
    evidence,
    agent_runs,
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(organizations.router)
api_router.include_router(users.router)
api_router.include_router(frameworks.router)
api_router.include_router(control_templates.router)
api_router.include_router(evidence_templates.router)
api_router.include_router(controls.router)
api_router.include_router(evidence.router)
api_router.include_router(agent_runs.router)
