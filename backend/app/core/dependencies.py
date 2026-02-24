from functools import wraps
from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session
from app.core.exceptions import ForbiddenError, NotFoundError, UnauthorizedError
from app.core.security import decode_token
from app.models.user import User


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedError("Missing or invalid authorization header")

    token = authorization.split(" ", 1)[1]
    payload = await decode_token(token)

    keycloak_id = payload.get("sub")
    if not keycloak_id:
        raise UnauthorizedError("Invalid token payload")

    result = await db.execute(select(User).where(User.keycloak_id == keycloak_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise NotFoundError("User not found. Please complete registration.")

    if not user.is_active:
        raise ForbiddenError("User account is deactivated")

    return user


async def get_optional_user(
    authorization: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_db),
) -> User | None:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    try:
        return await get_current_user(authorization=authorization, db=db)
    except Exception:
        return None


def require_role(*roles: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if current_user.role not in roles:
                raise ForbiddenError(
                    f"Role '{current_user.role}' does not have access. Required: {', '.join(roles)}"
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator


# Type aliases for dependency injection
DB = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


# ---------------------------------------------------------------------------
# Role constants
# ---------------------------------------------------------------------------
SUPER_ADMIN = "super_admin"
ADMIN = "admin"
COMPLIANCE_MANAGER = "compliance_manager"
CONTROL_OWNER = "control_owner"
EMPLOYEE = "employee"
EXECUTIVE = "executive"
AUDITOR_INTERNAL = "auditor_internal"
AUDITOR_EXTERNAL = "auditor_external"

ALL_ROLES = (
    SUPER_ADMIN,
    ADMIN,
    COMPLIANCE_MANAGER,
    CONTROL_OWNER,
    EMPLOYEE,
    EXECUTIVE,
    AUDITOR_INTERNAL,
    AUDITOR_EXTERNAL,
)

# Internal roles (everyone except external auditors)
INTERNAL_ROLES = (
    SUPER_ADMIN,
    ADMIN,
    COMPLIANCE_MANAGER,
    CONTROL_OWNER,
    EMPLOYEE,
    EXECUTIVE,
    AUDITOR_INTERNAL,
)


# ---------------------------------------------------------------------------
# RoleChecker – reusable FastAPI dependency
# ---------------------------------------------------------------------------
class RoleChecker:
    """FastAPI dependency that enforces role-based access control.

    Usage as a dependency:
        @router.get("/admin-only", dependencies=[Depends(RoleChecker(ADMIN, SUPER_ADMIN))])

    Or via Annotated type alias:
        async def endpoint(user: AdminUser): ...
    """

    def __init__(self, *allowed_roles: str) -> None:
        self.allowed_roles: set[str] = set(allowed_roles)

    async def __call__(
        self,
        current_user: User = Depends(get_current_user),
    ) -> User:
        # Super admins always pass
        if current_user.role == SUPER_ADMIN:
            return current_user

        if current_user.role not in self.allowed_roles:
            raise ForbiddenError(
                f"Role '{current_user.role}' does not have access. "
                f"Required: {', '.join(sorted(self.allowed_roles))}"
            )
        return current_user


# ---------------------------------------------------------------------------
# Convenience type aliases for common role checks
# ---------------------------------------------------------------------------
AdminUser = Annotated[User, Depends(RoleChecker(SUPER_ADMIN, ADMIN))]
ComplianceUser = Annotated[
    User, Depends(RoleChecker(SUPER_ADMIN, ADMIN, COMPLIANCE_MANAGER))
]
AnyInternalUser = Annotated[User, Depends(RoleChecker(*INTERNAL_ROLES))]
