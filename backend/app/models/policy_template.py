from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel, JSONType


class PolicyTemplate(BaseModel):
    __tablename__ = "policy_templates"

    template_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(100), nullable=False, default="Security")
    sections: Mapped[list | None] = mapped_column(JSONType(), default=list)
    variables: Mapped[list | None] = mapped_column(JSONType(), default=list)
    content_template: Mapped[str | None] = mapped_column(Text)
    required_by_frameworks: Mapped[list | None] = mapped_column(JSONType(), default=list)
    review_frequency: Mapped[str | None] = mapped_column(String(50))
