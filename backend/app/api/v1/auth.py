from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, get_current_user
from app.schemas.auth import TokenRequest, TokenResponse, UserInfo
from app.services.keycloak_service import keycloak_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
async def get_token(req: TokenRequest):
    data = await keycloak_service.exchange_token(req.username, req.password)
    return TokenResponse(
        access_token=data["access_token"],
        refresh_token=data.get("refresh_token"),
        token_type="bearer",
        expires_in=data.get("expires_in"),
    )


@router.get("/me", response_model=UserInfo)
async def get_me(current_user: CurrentUser):
    return UserInfo(
        keycloak_id=current_user.keycloak_id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        org_id=str(current_user.org_id),
    )


@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully. Clear tokens on client side."}
