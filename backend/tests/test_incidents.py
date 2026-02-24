import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Incidents Test Org", "slug": "incidents-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_list_incidents_empty(client: AsyncClient):
    resp = await client.get(f"/api/v1/organizations/{TEST_ORG_ID}/incidents")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_and_get_incident(client: AsyncClient):
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/incidents",
        json={
            "title": "Unauthorized Access Detected",
            "description": "Suspicious login from unknown IP",
            "severity": "P1",
            "status": "open",
            "category": "security",
        },
    )
    assert resp.status_code == 201
    incident_id = resp.json()["id"]
    data = resp.json()
    assert data["title"] == "Unauthorized Access Detected"
    assert data["severity"] == "P1"
    assert data["status"] == "open"

    get_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/incidents/{incident_id}"
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Unauthorized Access Detected"


@pytest.mark.asyncio
async def test_incident_stats(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/incidents/stats"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data
    assert "by_status" in data
    assert "by_severity" in data
    assert "open_p1_count" in data
    assert "avg_resolution_hours" in data


@pytest.mark.asyncio
async def test_add_timeline_event(client: AsyncClient):
    # Create incident first
    create_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/incidents",
        json={
            "title": "Database Outage",
            "description": "Primary database went down",
            "severity": "P2",
            "status": "open",
        },
    )
    assert create_resp.status_code == 201
    incident_id = create_resp.json()["id"]

    # Add timeline event
    event_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/incidents/{incident_id}/timeline",
        json={
            "event_type": "note",
            "description": "Database failover initiated",
        },
    )
    assert event_resp.status_code == 201
    event_data = event_resp.json()
    assert event_data["event_type"] == "note"
    assert event_data["description"] == "Database failover initiated"
    assert event_data["incident_id"] == incident_id

    # Get timeline
    timeline_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/incidents/{incident_id}/timeline"
    )
    assert timeline_resp.status_code == 200
    assert isinstance(timeline_resp.json(), list)
    assert len(timeline_resp.json()) >= 1
