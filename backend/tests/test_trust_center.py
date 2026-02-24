import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Trust Center Test Org", "slug": "trust-center-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_get_config(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/trust-center/config"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data
    assert data["org_id"] == TEST_ORG_ID
    assert "is_published" in data
    assert "slug" in data


@pytest.mark.asyncio
async def test_update_config(client: AsyncClient):
    # Ensure config exists first
    await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/trust-center/config"
    )

    update_resp = await client.patch(
        f"/api/v1/organizations/{TEST_ORG_ID}/trust-center/config",
        json={
            "headline": "QuickTrust Security & Compliance",
            "description": "Our commitment to security and compliance",
            "contact_email": "security@quicktrust.dev",
            "is_published": True,
            "certifications": ["SOC 2 Type II", "ISO 27001"],
        },
    )
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["headline"] == "QuickTrust Security & Compliance"
    assert data["is_published"] is True
    assert "SOC 2 Type II" in data["certifications"]


@pytest.mark.asyncio
async def test_create_document(client: AsyncClient):
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/trust-center/documents",
        json={
            "title": "SOC 2 Type II Report",
            "document_type": "audit_report",
            "is_public": False,
            "requires_nda": True,
            "description": "Our latest SOC 2 Type II audit report",
            "sort_order": 1,
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "SOC 2 Type II Report"
    assert data["document_type"] == "audit_report"
    assert data["is_public"] is False
    assert data["requires_nda"] is True

    # List documents
    list_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/trust-center/documents"
    )
    assert list_resp.status_code == 200
    assert isinstance(list_resp.json(), list)
    assert len(list_resp.json()) >= 1
