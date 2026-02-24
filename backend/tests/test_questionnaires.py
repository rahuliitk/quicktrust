import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Questionnaires Test Org", "slug": "questionnaires-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_list_questionnaires_empty(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/questionnaires"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_and_get_questionnaire(client: AsyncClient):
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/questionnaires",
        json={
            "title": "SOC 2 Vendor Questionnaire",
            "source": "customer_request",
            "status": "draft",
            "questions": [
                {"id": "q1", "text": "Do you encrypt data at rest?", "type": "yes_no"},
                {"id": "q2", "text": "Do you have a SOC 2 report?", "type": "yes_no"},
                {"id": "q3", "text": "Describe your access control process.", "type": "text"},
            ],
        },
    )
    assert resp.status_code == 201
    questionnaire_id = resp.json()["id"]
    data = resp.json()
    assert data["title"] == "SOC 2 Vendor Questionnaire"
    assert data["total_questions"] == 3

    get_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/questionnaires/{questionnaire_id}"
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "SOC 2 Vendor Questionnaire"


@pytest.mark.asyncio
async def test_auto_fill(client: AsyncClient):
    # Create questionnaire first
    create_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/questionnaires",
        json={
            "title": "Auto-Fill Test Questionnaire",
            "status": "in_progress",
            "questions": [
                {"id": "q1", "text": "Do you have an information security policy?", "type": "yes_no"},
            ],
        },
    )
    assert create_resp.status_code == 201
    questionnaire_id = create_resp.json()["id"]

    # Trigger auto-fill
    auto_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/questionnaires/{questionnaire_id}/auto-fill"
    )
    assert auto_resp.status_code == 200
    data = auto_resp.json()
    assert "message" in data


@pytest.mark.asyncio
async def test_questionnaire_stats(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/questionnaires/stats"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data
    assert "draft" in data
    assert "in_progress" in data
    assert "completed" in data
    assert "submitted" in data
