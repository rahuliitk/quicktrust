import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Controls Test Org", "slug": "controls-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_list_controls_empty(client: AsyncClient):
    resp = await client.get(f"/api/v1/organizations/{TEST_ORG_ID}/controls")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_and_get_control(client: AsyncClient):
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/controls",
        json={
            "title": "Test MFA Control",
            "description": "Enable MFA for all users",
            "status": "draft",
            "automation_level": "automated",
        },
    )
    assert resp.status_code == 201
    control_id = resp.json()["id"]

    get_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/controls/{control_id}"
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Test MFA Control"


@pytest.mark.asyncio
async def test_control_stats(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/controls/stats"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data
    assert "draft" in data
    assert "implemented" in data
