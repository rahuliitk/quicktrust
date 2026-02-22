from pydantic import BaseModel, EmailStr


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
    expires_in: int | None = None


class UserInfo(BaseModel):
    keycloak_id: str
    email: str
    full_name: str
    role: str
    org_id: str | None = None
