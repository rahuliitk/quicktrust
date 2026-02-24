import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Evidence Test Org", "slug": "evidence-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


async def _create_control(client: AsyncClient) -> str:
    """Helper to create a prerequisite control and return its ID."""
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/controls",
        json={
            "title": "Evidence Prerequisite Control",
            "description": "Control for evidence tests",
            "status": "draft",
            "automation_level": "manual",
        },
    )
    assert resp.status_code == 201
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_list_evidence_empty(client: AsyncClient):
    resp = await client.get(f"/api/v1/organizations/{TEST_ORG_ID}/evidence")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_evidence(client: AsyncClient):
    control_id = await _create_control(client)
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/evidence",
        json={
            "control_id": control_id,
            "title": "MFA Enrollment Screenshot",
            "status": "pending",
            "collection_method": "manual",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "MFA Enrollment Screenshot"
    assert data["control_id"] == control_id
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_get_evidence(client: AsyncClient):
    control_id = await _create_control(client)
    create_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/evidence",
        json={
            "control_id": control_id,
            "title": "CloudTrail Logs",
            "status": "collected",
            "collection_method": "automated",
            "collector": "aws_cloudtrail",
        },
    )
    assert create_resp.status_code == 201
    evidence_id = create_resp.json()["id"]

    get_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/evidence/{evidence_id}"
    )
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["title"] == "CloudTrail Logs"
    assert data["collector"] == "aws_cloudtrail"
    assert data["id"] == evidence_id
