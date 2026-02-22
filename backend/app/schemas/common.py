from uuid import UUID

from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 50

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int


class ErrorResponse(BaseModel):
    detail: str
    error_code: str | None = None


class MessageResponse(BaseModel):
    message: str


class IDResponse(BaseModel):
    id: UUID
