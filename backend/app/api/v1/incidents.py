from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser
from app.schemas.common import PaginatedResponse
from app.schemas.incident import (
    IncidentCreate,
    IncidentUpdate,
    IncidentResponse,
    IncidentStatsResponse,
    TimelineEventCreate,
    TimelineEventResponse,
)
from app.services import incident_service

router = APIRouter(
    prefix="/organizations/{org_id}/incidents",
    tags=["incidents"],
)


@router.get("", response_model=PaginatedResponse)
async def list_incidents(
    org_id: UUID,
    db: DB,
    current_user: AnyInternalUser,
    status: str | None = None,
    severity: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await incident_service.list_incidents(
        db, org_id, status=status, severity=severity, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[IncidentResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=IncidentResponse, status_code=201)
async def create_incident(org_id: UUID, data: IncidentCreate, db: DB, current_user: ComplianceUser):
    return await incident_service.create_incident(db, org_id, data)


@router.get("/stats", response_model=IncidentStatsResponse)
async def get_incident_stats(org_id: UUID, db: DB, current_user: AnyInternalUser):
    return await incident_service.get_incident_stats(db, org_id)


@router.get("/{incident_id}", response_model=IncidentResponse)
async def get_incident(org_id: UUID, incident_id: UUID, db: DB, current_user: AnyInternalUser):
    return await incident_service.get_incident(db, org_id, incident_id)


@router.patch("/{incident_id}", response_model=IncidentResponse)
async def update_incident(
    org_id: UUID, incident_id: UUID, data: IncidentUpdate, db: DB, current_user: ComplianceUser
):
    return await incident_service.update_incident(db, org_id, incident_id, data, actor_id=current_user.id)


@router.delete("/{incident_id}", status_code=204)
async def delete_incident(org_id: UUID, incident_id: UUID, db: DB, current_user: ComplianceUser):
    await incident_service.delete_incident(db, org_id, incident_id)


@router.post("/{incident_id}/timeline", response_model=TimelineEventResponse, status_code=201)
async def add_timeline_event(
    org_id: UUID, incident_id: UUID, data: TimelineEventCreate, db: DB, current_user: ComplianceUser
):
    return await incident_service.add_timeline_event(db, org_id, incident_id, data, actor_id=current_user.id)


@router.get("/{incident_id}/timeline", response_model=list[TimelineEventResponse])
async def get_timeline(org_id: UUID, incident_id: UUID, db: DB, current_user: AnyInternalUser):
    return await incident_service.get_timeline(db, org_id, incident_id)
