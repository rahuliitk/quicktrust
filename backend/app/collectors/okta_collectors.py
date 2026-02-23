"""Okta mock collectors for evidence auto-collection."""
from datetime import datetime, timezone
from typing import Any

from app.collectors.base import BaseCollector, register_collector


@register_collector("okta_mfa_enrollment")
class OktaMfaEnrollment(BaseCollector):
    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "Okta MFA enrollment report collected",
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
