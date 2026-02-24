import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Access Reviews Test Org", "slug": "access-reviews-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_list_campaigns_empty(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/access-reviews"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_and_get_campaign(client: AsyncClient):
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/access-reviews",
        json={
            "title": "Q1 2026 Access Review",
            "description": "Quarterly access review for all systems",
            "status": "draft",
        },
    )
    assert resp.status_code == 201
    campaign_id = resp.json()["id"]
    data = resp.json()
    assert data["title"] == "Q1 2026 Access Review"
    assert data["status"] == "draft"

    get_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/access-reviews/{campaign_id}"
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Q1 2026 Access Review"


@pytest.mark.asyncio
async def test_access_review_stats(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/access-reviews/stats"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "total_campaigns" in data
    assert "active_campaigns" in data
    assert "total_entries" in data
    assert "pending_decisions" in data
    assert "approved" in data
    assert "revoked" in data


@pytest.mark.asyncio
async def test_create_and_update_entry(client: AsyncClient):
    # Create campaign first
    campaign_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/access-reviews",
        json={
            "title": "Engineering Access Review",
            "description": "Review engineering team access",
            "status": "active",
        },
    )
    assert campaign_resp.status_code == 201
    campaign_id = campaign_resp.json()["id"]

    # Create entry
    entry_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/access-reviews/{campaign_id}/entries",
        json={
            "user_name": "Jane Developer",
            "user_email": "jane@example.com",
            "system_name": "AWS Console",
            "resource": "Production Account",
            "current_access": "admin",
        },
    )
    assert entry_resp.status_code == 201
    entry_id = entry_resp.json()["id"]
    assert entry_resp.json()["user_name"] == "Jane Developer"
    assert entry_resp.json()["system_name"] == "AWS Console"

    # Update entry with decision
    update_resp = await client.patch(
        f"/api/v1/organizations/{TEST_ORG_ID}/access-reviews/{campaign_id}/entries/{entry_id}",
        json={
            "decision": "approved",
            "notes": "Access verified and appropriate",
        },
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["decision"] == "approved"
