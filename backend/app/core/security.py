import httpx
from jose import JWTError, jwt
from functools import lru_cache

from app.config import get_settings
from app.core.exceptions import UnauthorizedError

settings = get_settings()

_jwks_cache: dict | None = None


async def get_jwks() -> dict:
    global _jwks_cache
    if _jwks_cache is not None:
        return _jwks_cache

    jwks_url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
    async with httpx.AsyncClient() as client:
        resp = await client.get(jwks_url)
        resp.raise_for_status()
        _jwks_cache = resp.json()
        return _jwks_cache


def clear_jwks_cache():
    global _jwks_cache
    _jwks_cache = None


async def decode_token(token: str) -> dict:
    try:
        jwks = await get_jwks()
        # Get the header to find the key id
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        # Find the matching key
        rsa_key = None
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                rsa_key = key
                break

        if rsa_key is None:
            # Try refreshing JWKS cache
            clear_jwks_cache()
            jwks = await get_jwks()
            for key in jwks.get("keys", []):
                if key.get("kid") == kid:
                    rsa_key = key
                    break

        if rsa_key is None:
            raise UnauthorizedError("Unable to find signing key")

        issuer = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}"

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience="account",
            issuer=issuer,
            options={"verify_aud": False},
        )
        return payload

    except JWTError as e:
        raise UnauthorizedError(f"Invalid token: {str(e)}")
    except httpx.HTTPError:
        raise UnauthorizedError("Could not validate credentials (Keycloak unreachable)")
