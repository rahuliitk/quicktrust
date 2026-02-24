import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Training Test Org", "slug": "training-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_list_courses_empty(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/training/courses"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_and_get_course(client: AsyncClient):
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/training/courses",
        json={
            "title": "Security Awareness Training",
            "description": "Annual security training for all employees",
            "course_type": "document",
            "duration_minutes": 60,
            "is_required": True,
            "is_active": True,
        },
    )
    assert resp.status_code == 201
    course_id = resp.json()["id"]
    data = resp.json()
    assert data["title"] == "Security Awareness Training"
    assert data["is_required"] is True
    assert data["duration_minutes"] == 60

    get_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/training/courses/{course_id}"
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Security Awareness Training"


@pytest.mark.asyncio
async def test_training_stats(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/training/assignments/stats"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "total_courses" in data
    assert "assigned" in data
    assert "completed" in data
    assert "overdue" in data
    assert "completion_rate_pct" in data
