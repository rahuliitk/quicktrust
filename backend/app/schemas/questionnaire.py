from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class QuestionnaireCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    source: str | None = None
    status: str = "draft"
    questions: list[dict] | None = None


class QuestionnaireUpdate(BaseModel):
    title: str | None = None
    source: str | None = None
    status: str | None = None
    questions: list[dict] | None = None


class QuestionResponseCreate(BaseModel):
    question_id: str
    question_text: str
    answer: str | None = None
    confidence: float | None = None
    source_type: str | None = None
    source_id: UUID | None = None


class QuestionResponseUpdate(BaseModel):
    answer: str | None = None
    confidence: float | None = None
    source_type: str | None = None
    source_id: UUID | None = None
    is_approved: bool | None = None


class QuestionResponseRead(BaseModel):
    id: UUID
    questionnaire_id: UUID
    org_id: UUID
    question_id: str
    question_text: str
    answer: str | None
    confidence: float | None
    source_type: str | None
    source_id: UUID | None
    is_approved: bool
    approved_by_id: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class QuestionnaireDetailResponse(BaseModel):
    id: UUID
    org_id: UUID
    title: str
    source: str | None
    status: str
    questions: list | None
    total_questions: int
    answered_count: int
    responses: list[QuestionResponseRead] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class QuestionnaireStatsResponse(BaseModel):
    total: int = 0
    draft: int = 0
    in_progress: int = 0
    completed: int = 0
    submitted: int = 0
