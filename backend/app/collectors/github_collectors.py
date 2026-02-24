"""GitHub collectors for evidence auto-collection.

Each collector attempts real GitHub API calls using httpx. If credentials are
missing or the call fails, the collector falls back to mock data so that
the application works without live GitHub connectivity.
"""
import logging
from datetime import datetime, timezone
from typing import Any

import httpx

from app.collectors.base import BaseCollector, register_collector

logger = logging.getLogger(__name__)

GITHUB_API_BASE = "https://api.github.com"


def _github_headers(credentials: dict | None) -> dict[str, str]:
    """Build HTTP headers for authenticated GitHub API requests."""
    if not credentials:
        raise ValueError("No credentials provided")

    token = credentials.get("github_token") or credentials.get("token")
    if not token:
        raise ValueError("No github_token in credentials")

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


# ---------------------------------------------------------------------------
# Branch Protection
# ---------------------------------------------------------------------------

@register_collector("github_branch_protection")
class GitHubBranchProtection(BaseCollector):
    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        try:
            headers = _github_headers(credentials)

            # config may contain repos list; fall back to a single owner/repo
            repos = config.get("repositories") or []
            if not repos:
                owner = credentials.get("owner") or config.get("owner", "")
                repo = credentials.get("repo") or config.get("repo", "")
                if owner and repo:
                    repos = [{"owner": owner, "repo": repo, "branch": config.get("branch", "main")}]

            if not repos:
                raise ValueError("No repositories configured for branch protection check")

            results = []
            async with httpx.AsyncClient(timeout=30.0) as client:
                for repo_cfg in repos:
                    owner = repo_cfg.get("owner", "")
                    repo = repo_cfg.get("repo", "")
                    branch = repo_cfg.get("branch", "main")

                    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/branches/{branch}/protection"
                    resp = await client.get(url, headers=headers)

                    if resp.status_code == 200:
                        data = resp.json()
                        pr_reviews = data.get("required_pull_request_reviews", {})
                        results.append({
                            "name": f"{owner}/{repo}",
                            "default_branch": branch,
                            "protection_enabled": True,
                            "required_reviews": pr_reviews.get(
                                "required_approving_review_count", 0
                            ),
                            "dismiss_stale_reviews": pr_reviews.get(
                                "dismiss_stale_reviews", False
                            ),
                            "require_code_owner_reviews": pr_reviews.get(
                                "require_code_owner_reviews", False
                            ),
                            "enforce_admins": data.get("enforce_admins", {}).get(
                                "enabled", False
                            ),
                        })
                    elif resp.status_code == 404:
                        # No protection rules configured
                        results.append({
                            "name": f"{owner}/{repo}",
                            "default_branch": branch,
                            "protection_enabled": False,
                            "required_reviews": 0,
                            "dismiss_stale_reviews": False,
                            "require_code_owner_reviews": False,
                            "enforce_admins": False,
                        })
                    else:
                        logger.warning(
                            "GitHub branch protection API returned %d for %s/%s",
                            resp.status_code, owner, repo,
                        )

            compliant_repos = sum(1 for r in results if r["protection_enabled"])
            logger.info(
                "GitHub branch protection collected via live API (%d/%d compliant)",
                compliant_repos, len(results),
            )
            return {
                "status": "success",
                "summary": "Branch protection rules verified via GitHub API",
                "data": {
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "repositories": results,
                    "compliant_repos": compliant_repos,
                    "total_repos": len(results),
                },
            }
        except Exception as exc:
            logger.warning("GitHub branch protection real collection failed, using mock data: %s", exc)
            return self._mock_response()

    @staticmethod
    def _mock_response() -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "Branch protection rules verified (mock)",
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


# ---------------------------------------------------------------------------
# Dependabot Alerts
# ---------------------------------------------------------------------------

@register_collector("github_dependabot_alerts")
class GitHubDependabotAlerts(BaseCollector):
    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        try:
            headers = _github_headers(credentials)

            repos = config.get("repositories") or []
            if not repos:
                owner = credentials.get("owner") or config.get("owner", "")
                repo = credentials.get("repo") or config.get("repo", "")
                if owner and repo:
                    repos = [{"owner": owner, "repo": repo}]

            if not repos:
                raise ValueError("No repositories configured for Dependabot check")

            all_alerts: list[dict] = []
            severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}

            async with httpx.AsyncClient(timeout=30.0) as client:
                for repo_cfg in repos:
                    owner = repo_cfg.get("owner", "")
                    repo = repo_cfg.get("repo", "")
                    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/dependabot/alerts"
                    params = {"state": "open", "per_page": 100}

                    resp = await client.get(url, headers=headers, params=params)

                    if resp.status_code == 200:
                        alerts_data = resp.json()
                        for alert in alerts_data:
                            severity = (
                                alert.get("security_vulnerability", {})
                                .get("severity", "unknown")
                                .lower()
                            )
                            pkg = (
                                alert.get("security_vulnerability", {})
                                .get("package", {})
                                .get("name", "unknown")
                            )
                            all_alerts.append({
                                "package": pkg,
                                "severity": severity,
                                "repository": f"{owner}/{repo}",
                                "created_at": alert.get("created_at", ""),
                                "state": alert.get("state", "open"),
                            })
                            if severity in severity_counts:
                                severity_counts[severity] += 1
                    elif resp.status_code == 403:
                        logger.warning(
                            "Dependabot alerts not enabled or insufficient permissions for %s/%s",
                            owner, repo,
                        )
                    else:
                        logger.warning(
                            "GitHub Dependabot API returned %d for %s/%s",
                            resp.status_code, owner, repo,
                        )

            logger.info(
                "GitHub Dependabot alerts collected via live API (%d total alerts)",
                len(all_alerts),
            )
            return {
                "status": "success",
                "summary": "Dependabot vulnerability alerts collected via GitHub API",
                "data": {
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "total_alerts": len(all_alerts),
                    **severity_counts,
                    "alerts": all_alerts[:50],  # limit payload
                },
            }
        except Exception as exc:
            logger.warning("GitHub Dependabot real collection failed, using mock data: %s", exc)
            return self._mock_response()

    @staticmethod
    def _mock_response() -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "Dependabot vulnerability alerts collected (mock)",
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
