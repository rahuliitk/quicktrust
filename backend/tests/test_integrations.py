import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Integrations Test Org", "slug": "integrations-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_list_integrations_empty(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/integrations"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_and_get_integration(client: AsyncClient):
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/integrations",
        json={
            "provider": "aws",
            "name": "AWS Production Account",
            "config": {"region": "us-east-1", "account_id": "123456789012"},
            "credentials_ref": "vault://aws/prod",
        },
    )
    assert resp.status_code == 201
    integration_id = resp.json()["id"]
    data = resp.json()
    assert data["provider"] == "aws"
    assert data["name"] == "AWS Production Account"
    assert data["config"]["region"] == "us-east-1"

    get_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/integrations/{integration_id}"
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "AWS Production Account"


@pytest.mark.asyncio
async def test_list_providers(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/integrations/providers"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    # Verify known providers exist
    provider_names = [p["provider"] for p in data]
    assert "aws" in provider_names
    assert "github" in provider_names

    # Verify each provider has expected fields
    for provider in data:
        assert "provider" in provider
        assert "name" in provider
        assert "description" in provider
        assert "collector_types" in provider
