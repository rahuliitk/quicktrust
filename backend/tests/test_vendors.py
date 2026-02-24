import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Vendors Test Org", "slug": "vendors-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_list_vendors_empty(client: AsyncClient):
    resp = await client.get(f"/api/v1/organizations/{TEST_ORG_ID}/vendors")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_and_get_vendor(client: AsyncClient):
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/vendors",
        json={
            "name": "Acme Cloud Provider",
            "category": "cloud_infrastructure",
            "website": "https://acme.example.com",
            "risk_tier": "high",
            "status": "active",
            "contact_name": "John Doe",
            "contact_email": "john@acme.example.com",
        },
    )
    assert resp.status_code == 201
    vendor_id = resp.json()["id"]
    data = resp.json()
    assert data["name"] == "Acme Cloud Provider"
    assert data["risk_tier"] == "high"
    assert data["status"] == "active"

    get_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/vendors/{vendor_id}"
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Acme Cloud Provider"


@pytest.mark.asyncio
async def test_vendor_stats(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/vendors/stats"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data
    assert "by_risk_tier" in data
    assert "by_status" in data
    assert "expiring_contracts_count" in data


@pytest.mark.asyncio
async def test_create_vendor_assessment(client: AsyncClient):
    # Create vendor first
    vendor_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/vendors",
        json={
            "name": "SecureAuth Vendor",
            "category": "identity",
            "risk_tier": "medium",
            "status": "active",
        },
    )
    assert vendor_resp.status_code == 201
    vendor_id = vendor_resp.json()["id"]

    # Create assessment
    assess_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/vendors/{vendor_id}/assessments",
        json={
            "score": 85,
            "risk_tier_assigned": "low",
            "notes": "Vendor meets all security requirements",
            "questionnaire_data": {"encryption": True, "soc2": True},
        },
    )
    assert assess_resp.status_code == 201
    assess_data = assess_resp.json()
    assert assess_data["score"] == 85
    assert assess_data["risk_tier_assigned"] == "low"
    assert assess_data["vendor_id"] == vendor_id

    # List assessments
    list_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/vendors/{vendor_id}/assessments"
    )
    assert list_resp.status_code == 200
    assert isinstance(list_resp.json(), list)
    assert len(list_resp.json()) >= 1
