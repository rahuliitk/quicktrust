"""Okta collectors for evidence auto-collection.

Each collector attempts real Okta API calls using httpx. If credentials are
missing or the call fails, the collector falls back to mock data so that
the application works without live Okta connectivity.
"""
import logging
from datetime import datetime, timezone
from typing import Any

import httpx

from app.collectors.base import BaseCollector, register_collector

logger = logging.getLogger(__name__)


def _okta_headers(credentials: dict | None) -> tuple[str, dict[str, str]]:
    """Return (base_url, headers) for authenticated Okta API requests."""
    if not credentials:
        raise ValueError("No credentials provided")

    token = credentials.get("okta_token") or credentials.get("token")
    domain = credentials.get("okta_domain") or credentials.get("domain")

    if not token or not domain:
        raise ValueError("okta_token and okta_domain are required in credentials")

    # Normalise domain to base URL
    base_url = domain if domain.startswith("https://") else f"https://{domain}"
    base_url = base_url.rstrip("/")

    headers = {
        "Authorization": f"SSWS {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    return base_url, headers


# ---------------------------------------------------------------------------
# Okta MFA Enrollment
# ---------------------------------------------------------------------------

@register_collector("okta_mfa_enrollment")
class OktaMfaEnrollment(BaseCollector):
    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        try:
            base_url, headers = _okta_headers(credentials)

            # Fetch active users with pagination
            all_users: list[dict] = []
            url = f"{base_url}/api/v1/users"
            params: dict[str, Any] = {
                "filter": 'status eq "ACTIVE"',
                "limit": 200,
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                while url:
                    resp = await client.get(url, headers=headers, params=params)
                    resp.raise_for_status()
                    all_users.extend(resp.json())

                    # Okta uses Link headers for pagination
                    url = None
                    params = {}  # params already in the link
                    link_header = resp.headers.get("Link", "")
                    for part in link_header.split(","):
                        if 'rel="next"' in part:
                            url = part.split(";")[0].strip().strip("<>")
                            break

            # For each user, fetch enrolled factors
            mfa_enrolled = 0
            mfa_not_enrolled = 0
            factor_counts: dict[str, int] = {}
            non_enrolled_users: list[dict] = []

            async with httpx.AsyncClient(timeout=30.0) as client:
                for user in all_users:
                    user_id = user.get("id")
                    email = user.get("profile", {}).get("email", "unknown")

                    factors_url = f"{base_url}/api/v1/users/{user_id}/factors"
                    try:
                        factors_resp = await client.get(factors_url, headers=headers)
                        factors_resp.raise_for_status()
                        factors = factors_resp.json()
                    except Exception:
                        factors = []

                    active_factors = [
                        f for f in factors if f.get("status") == "ACTIVE"
                    ]
                    if active_factors:
                        mfa_enrolled += 1
                        for f in active_factors:
                            provider = f.get("provider", "unknown").lower()
                            factor_counts[provider] = factor_counts.get(provider, 0) + 1
                    else:
                        mfa_not_enrolled += 1
                        non_enrolled_users.append({
                            "email": email,
                            "status": user.get("status", "ACTIVE"),
                        })

            total_users = len(all_users)
            enrollment_rate = round(
                (mfa_enrolled / total_users * 100), 1
            ) if total_users > 0 else 0.0

            logger.info(
                "Okta MFA enrollment collected via live API (%d users, %.1f%% enrolled)",
                total_users, enrollment_rate,
            )
            return {
                "status": "success",
                "summary": "Okta MFA enrollment report collected via Okta API",
                "data": {
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "total_users": total_users,
                    "mfa_enrolled": mfa_enrolled,
                    "mfa_not_enrolled": mfa_not_enrolled,
                    "enrollment_rate": enrollment_rate,
                    "mfa_factors": factor_counts,
                    "non_enrolled_users": non_enrolled_users[:20],  # limit payload
                },
            }
        except Exception as exc:
            logger.warning("Okta MFA real collection failed, using mock data: %s", exc)
            return self._mock_response()

    @staticmethod
    def _mock_response() -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "Okta MFA enrollment report collected (mock)",
            "data": {
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "total_users": 120,
                "mfa_enrolled": 118,
                "mfa_not_enrolled": 2,
                "enrollment_rate": 98.3,
                "mfa_factors": {
                    "okta_verify": 95,
                    "google_authenticator": 15,
                    "yubikey": 8,
                },
                "non_enrolled_users": [
                    {"email": "new.hire@company.com", "status": "PENDING"},
                    {"email": "contractor@partner.com", "status": "ACTIVE"},
                ],
            },
        }
