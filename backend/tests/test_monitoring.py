import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Monitoring Test Org", "slug": "monitoring-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_list_rules_empty(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/monitoring/rules"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_and_get_rule(client: AsyncClient):
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/monitoring/rules",
        json={
            "title": "MFA Enrollment Check",
            "description": "Check that all users have MFA enabled",
            "check_type": "manual",
            "schedule": "daily",
            "is_active": True,
            "config": {"threshold": 100},
        },
    )
    assert resp.status_code == 201
    rule_id = resp.json()["id"]
    data = resp.json()
    assert data["title"] == "MFA Enrollment Check"
    assert data["check_type"] == "manual"
    assert data["is_active"] is True

    get_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/monitoring/rules/{rule_id}"
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "MFA Enrollment Check"


@pytest.mark.asyncio
async def test_run_checks(client: AsyncClient):
    # Create rule first
    rule_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/monitoring/rules",
        json={
            "title": "Encryption At Rest Check",
            "description": "Verify encryption at rest is enabled",
            "check_type": "manual",
            "schedule": "weekly",
            "is_active": True,
        },
    )
    assert rule_resp.status_code == 201
    rule_id = rule_resp.json()["id"]

    # Run checks
    run_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/monitoring/rules/{rule_id}/run"
    )
    assert run_resp.status_code == 200
    assert isinstance(run_resp.json(), list)


@pytest.mark.asyncio
async def test_monitoring_stats(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/monitoring/stats"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "total_rules" in data
    assert "active_rules" in data
    assert "open_alerts" in data
    assert "by_severity" in data
