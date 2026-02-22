from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ControlTemplateResponse(BaseModel):
    id: UUID
    template_code: str
    title: str
    domain: str
    description: str | None
    implementation_guidance: str | None
    test_procedure: str | None
    automation_level: str
    variables: dict | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ControlTemplateBriefResponse(BaseModel):
    id: UUID
    template_code: str
    title: str
    domain: str
    automation_level: str

    model_config = {"from_attributes": True}
