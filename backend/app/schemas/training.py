from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TrainingCourseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = None
    content_url: str | None = None
    course_type: str = "document"
    required_roles: list[str] | None = None
    duration_minutes: int | None = None
    is_required: bool = False
    is_active: bool = True


class TrainingCourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    content_url: str | None = None
    course_type: str | None = None
    required_roles: list[str] | None = None
    duration_minutes: int | None = None
    is_required: bool | None = None
    is_active: bool | None = None


class TrainingCourseResponse(BaseModel):
    id: UUID
    org_id: UUID
    title: str
    description: str | None
    content_url: str | None
    course_type: str
    required_roles: list | None
    duration_minutes: int | None
    is_required: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TrainingAssignmentCreate(BaseModel):
    course_id: UUID
    user_id: UUID
    due_date: datetime | None = None


class TrainingAssignmentUpdate(BaseModel):
    status: str | None = None
    score: int | None = None
    attempts: int | None = None


class TrainingAssignmentResponse(BaseModel):
    id: UUID
    org_id: UUID
    course_id: UUID
    user_id: UUID
    status: str
    due_date: datetime | None
    completed_at: datetime | None
    score: int | None
    attempts: int
    assigned_by_id: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TrainingStatsResponse(BaseModel):
    total_courses: int = 0
    assigned: int = 0
    completed: int = 0
    overdue: int = 0
    completion_rate_pct: float = 0.0
