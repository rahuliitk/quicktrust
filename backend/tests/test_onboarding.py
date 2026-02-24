import uuid

import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Onboarding Test Org", "slug": "onboarding-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_start_onboarding(client: AsyncClient):
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/onboarding/start",
        json={
            "company_name": "Test Corp",
            "industry": "technology",
            "company_size": "50-100",
            "cloud_providers": ["aws", "gcp"],
            "tech_stack": ["python", "react", "postgres"],
            "departments": ["engineering", "finance", "legal"],
            "target_framework_ids": [],
            "compliance_timeline": "6 months",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["org_id"] == TEST_ORG_ID
    assert data["status"] in ("pending", "running", "completed")
    assert "input_data" in data
    assert "id" in data


@pytest.mark.asyncio
async def test_get_latest_onboarding(client: AsyncClient):
    # First, start an onboarding session
    await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/onboarding/start",
        json={
            "company_name": "Latest Test Corp",
            "industry": "healthcare",
            "company_size": "100-500",
            "cloud_providers": ["azure"],
            "tech_stack": ["java", "angular"],
            "departments": ["engineering"],
            "target_framework_ids": [],
        },
    )

    # Get latest
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/onboarding/latest"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data is not None
    assert data["org_id"] == TEST_ORG_ID
    assert "status" in data
    assert "input_data" in data
