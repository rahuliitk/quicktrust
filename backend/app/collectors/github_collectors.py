"""GitHub mock collectors for evidence auto-collection."""
from datetime import datetime, timezone
from typing import Any

from app.collectors.base import BaseCollector, register_collector


@register_collector("github_branch_protection")
class GitHubBranchProtection(BaseCollector):
    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "Branch protection rules verified",
            "data": {
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "repositories": [
                    {
                        "name": "backend-api",
                        "default_branch": "main",
                        "protection_enabled": True,
                        "required_reviews": 2,
                        "dismiss_stale_reviews": True,
                        "require_code_owner_reviews": True,
                        "enforce_admins": True,
                    },
                    {
                        "name": "frontend-app",
                        "default_branch": "main",
                        "protection_enabled": True,
                        "required_reviews": 1,
                        "dismiss_stale_reviews": True,
                        "require_code_owner_reviews": False,
                        "enforce_admins": True,
                    },
                ],
                "compliant_repos": 2,
                "total_repos": 2,
            },
        }


@register_collector("github_dependabot_alerts")
class GitHubDependabotAlerts(BaseCollector):
    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "Dependabot vulnerability alerts collected",
            "data": {
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "total_alerts": 7,
                "critical": 0,
                "high": 1,
                "medium": 3,
                "low": 3,
                "alerts": [
                    {
                        "package": "lodash",
                        "severity": "high",
                        "repository": "backend-api",
                        "created_at": "2026-01-10",
                        "state": "open",
                    },
                ],
            },
        }
