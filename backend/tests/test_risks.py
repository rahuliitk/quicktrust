import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Risks Test Org", "slug": "risks-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_list_risks_empty(client: AsyncClient):
    resp = await client.get(f"/api/v1/organizations/{TEST_ORG_ID}/risks")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_and_get_risk(client: AsyncClient):
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/risks",
        json={
            "title": "Unauthorized Data Access",
            "description": "Risk of unauthorized access to customer data",
            "category": "security",
            "likelihood": 4,
            "impact": 5,
            "status": "identified",
        },
    )
    assert resp.status_code == 201
    risk_id = resp.json()["id"]
    data = resp.json()
    assert data["title"] == "Unauthorized Data Access"
    assert data["likelihood"] == 4
    assert data["impact"] == 5
    assert "risk_score" in data
    assert "risk_level" in data

    get_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/risks/{risk_id}"
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Unauthorized Data Access"


@pytest.mark.asyncio
async def test_risk_stats(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/risks/stats"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data
    assert "by_status" in data
    assert "by_risk_level" in data
    assert "average_score" in data


@pytest.mark.asyncio
async def test_risk_matrix(client: AsyncClient):
    # Create a risk first so the matrix has data
    await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/risks",
        json={
            "title": "Phishing Attack",
            "description": "Risk of phishing attacks on employees",
            "category": "security",
            "likelihood": 3,
            "impact": 4,
            "status": "identified",
        },
    )

    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/risks/matrix"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "cells" in data
    assert isinstance(data["cells"], list)
