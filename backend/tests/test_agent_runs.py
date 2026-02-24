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
        json={"name": "Agent Runs Test Org", "slug": "agent-runs-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_list_agent_runs_empty(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/agents/runs"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_trigger_controls_generation(client: AsyncClient):
    """Trigger controls generation agent. The agent run record should be created
    even if the background LLM task fails (since it runs asynchronously)."""
    framework_id = str(uuid.uuid4())
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/agents/controls-generation/run",
        json={
            "framework_id": framework_id,
            "company_context": {
                "industry": "technology",
                "size": "startup",
            },
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["agent_type"] == "controls_generation"
    assert data["trigger"] == "manual"
    assert data["status"] == "pending"
    assert data["org_id"] == TEST_ORG_ID
    assert data["input_data"]["framework_id"] == framework_id
    assert "id" in data


@pytest.mark.asyncio
async def test_get_agent_run(client: AsyncClient):
    """Create an agent run and then retrieve it by ID."""
    framework_id = str(uuid.uuid4())
    create_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/agents/controls-generation/run",
        json={
            "framework_id": framework_id,
            "company_context": {"industry": "finance"},
        },
    )
    assert create_resp.status_code == 201
    run_id = create_resp.json()["id"]

    get_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/agents/runs/{run_id}"
    )
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == run_id
    assert data["agent_type"] == "controls_generation"
    assert data["org_id"] == TEST_ORG_ID
