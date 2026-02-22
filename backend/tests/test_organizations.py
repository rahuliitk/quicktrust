import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_organization(client: AsyncClient):
    resp = await client.post(
        "/api/v1/organizations",
        json={
            "name": "Test Org",
            "slug": "test-org",
            "industry": "Technology",
            "company_size": "50-200",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Test Org"
    assert data["slug"] == "test-org"
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_get_organization(client: AsyncClient):
    # Create first
    create_resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Get Org", "slug": "get-org"},
    )
    org_id = create_resp.json()["id"]

    # Then get
    resp = await client.get(f"/api/v1/organizations/{org_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Get Org"


@pytest.mark.asyncio
async def test_update_organization(client: AsyncClient):
    create_resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Update Org", "slug": "update-org"},
    )
    org_id = create_resp.json()["id"]

    resp = await client.patch(
        f"/api/v1/organizations/{org_id}",
        json={"industry": "Healthcare"},
    )
    assert resp.status_code == 200
    assert resp.json()["industry"] == "Healthcare"
