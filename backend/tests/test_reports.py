import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Reports Test Org", "slug": "reports-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_list_reports_empty(client: AsyncClient):
    resp = await client.get(f"/api/v1/organizations/{TEST_ORG_ID}/reports")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_and_get_report(client: AsyncClient):
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/reports",
        json={
            "title": "Q1 Compliance Summary",
            "report_type": "compliance_summary",
            "format": "json",
            "parameters": {"quarter": "Q1", "year": 2026},
        },
    )
    assert resp.status_code == 201
    report_id = resp.json()["id"]
    data = resp.json()
    assert data["title"] == "Q1 Compliance Summary"
    assert data["report_type"] == "compliance_summary"
    assert data["format"] == "json"

    get_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/reports/{report_id}"
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Q1 Compliance Summary"


@pytest.mark.asyncio
async def test_generate_report(client: AsyncClient):
    # Create report first
    create_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/reports",
        json={
            "title": "Risk Assessment Report",
            "report_type": "risk_assessment",
            "format": "json",
        },
    )
    assert create_resp.status_code == 201
    report_id = create_resp.json()["id"]

    # Get report data (generate)
    data_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/reports/{report_id}/data"
    )
    assert data_resp.status_code == 200


@pytest.mark.asyncio
async def test_report_stats(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/reports/stats"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data
    assert "by_type" in data
    assert "by_status" in data
