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
    policies,
    policy_templates,
    risks,
    integrations,
    audits,
    auditor_portal,
    onboarding,
    incidents,
    vendors,
    training,
    access_reviews,
    monitoring,
    questionnaires,
    trust_center,
    reports,
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
api_router.include_router(policies.router)
api_router.include_router(policy_templates.router)
api_router.include_router(risks.router)
api_router.include_router(integrations.router)
api_router.include_router(audits.router)
api_router.include_router(auditor_portal.router)
api_router.include_router(onboarding.router)
api_router.include_router(incidents.router)
api_router.include_router(vendors.router)
api_router.include_router(training.router)
api_router.include_router(access_reviews.router)
api_router.include_router(monitoring.router)
api_router.include_router(questionnaires.router)
api_router.include_router(trust_center.router)
api_router.include_router(reports.router)
api_router.include_router(trust_center.public_router)
