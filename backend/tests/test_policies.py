import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Policies Test Org", "slug": "policies-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_list_policies_empty(client: AsyncClient):
    resp = await client.get(f"/api/v1/organizations/{TEST_ORG_ID}/policies")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_and_get_policy(client: AsyncClient):
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/policies",
        json={
            "title": "Acceptable Use Policy",
            "content": "All employees must follow acceptable use guidelines.",
            "status": "draft",
            "version": "1.0",
        },
    )
    assert resp.status_code == 201
    policy_id = resp.json()["id"]
    assert resp.json()["title"] == "Acceptable Use Policy"

    get_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/policies/{policy_id}"
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Acceptable Use Policy"
    assert get_resp.json()["version"] == "1.0"


@pytest.mark.asyncio
async def test_policy_stats(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/policies/stats"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data
    assert "draft" in data
    assert "published" in data
    assert "archived" in data


@pytest.mark.asyncio
async def test_update_policy_status(client: AsyncClient):
    create_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/policies",
        json={
            "title": "Data Retention Policy",
            "content": "Data retention requirements.",
            "status": "draft",
        },
    )
    assert create_resp.status_code == 201
    policy_id = create_resp.json()["id"]

    update_resp = await client.patch(
        f"/api/v1/organizations/{TEST_ORG_ID}/policies/{policy_id}",
        json={"title": "Data Retention Policy v2", "content": "Updated retention requirements."},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "Data Retention Policy v2"
