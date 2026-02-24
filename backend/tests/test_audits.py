from datetime import datetime, timezone, timedelta

import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Audits Test Org", "slug": "audits-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_list_audits_empty(client: AsyncClient):
    resp = await client.get(f"/api/v1/organizations/{TEST_ORG_ID}/audits")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_and_get_audit(client: AsyncClient):
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/audits",
        json={
            "title": "SOC 2 Type II Audit 2026",
            "audit_type": "external",
            "auditor_firm": "Big Four Auditors LLP",
            "lead_auditor_name": "Jane Auditor",
        },
    )
    assert resp.status_code == 201
    audit_id = resp.json()["id"]
    data = resp.json()
    assert data["title"] == "SOC 2 Type II Audit 2026"
    assert data["audit_type"] == "external"
    assert data["auditor_firm"] == "Big Four Auditors LLP"

    get_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/audits/{audit_id}"
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "SOC 2 Type II Audit 2026"


@pytest.mark.asyncio
async def test_create_finding(client: AsyncClient):
    # Create audit first
    audit_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/audits",
        json={
            "title": "Internal Audit Q1",
            "audit_type": "internal",
        },
    )
    assert audit_resp.status_code == 201
    audit_id = audit_resp.json()["id"]

    # Create finding
    finding_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/audits/{audit_id}/findings",
        json={
            "title": "Missing MFA on Admin Accounts",
            "description": "Several admin accounts lack MFA enforcement",
            "severity": "high",
            "status": "open",
            "remediation_plan": "Enable MFA for all admin accounts within 30 days",
        },
    )
    assert finding_resp.status_code == 201
    finding_data = finding_resp.json()
    assert finding_data["title"] == "Missing MFA on Admin Accounts"
    assert finding_data["severity"] == "high"
    assert finding_data["audit_id"] == audit_id

    # List findings
    list_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/audits/{audit_id}/findings"
    )
    assert list_resp.status_code == 200
    assert isinstance(list_resp.json(), list)
    assert len(list_resp.json()) >= 1


@pytest.mark.asyncio
async def test_create_and_revoke_token(client: AsyncClient):
    # Create audit first
    audit_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/audits",
        json={
            "title": "Token Test Audit",
            "audit_type": "external",
        },
    )
    assert audit_resp.status_code == 201
    audit_id = audit_resp.json()["id"]

    # Create access token
    expires = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    token_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/audits/{audit_id}/tokens",
        json={
            "auditor_email": "external.auditor@audit-firm.com",
            "auditor_name": "External Auditor",
            "permissions": {"read_evidence": True, "read_controls": True},
            "expires_at": expires,
        },
    )
    assert token_resp.status_code == 201
    token_data = token_resp.json()
    assert token_data["auditor_email"] == "external.auditor@audit-firm.com"
    assert token_data["is_active"] is True
    token_id = token_data["id"]

    # List tokens
    list_resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/audits/{audit_id}/tokens"
    )
    assert list_resp.status_code == 200
    assert isinstance(list_resp.json(), list)
    assert len(list_resp.json()) >= 1

    # Revoke token
    revoke_resp = await client.delete(
        f"/api/v1/organizations/{TEST_ORG_ID}/audits/{audit_id}/tokens/{token_id}"
    )
    assert revoke_resp.status_code == 204


@pytest.mark.asyncio
async def test_readiness_score(client: AsyncClient):
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/audits/readiness"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "overall_score" in data
    assert "controls_score" in data
    assert "evidence_score" in data
    assert "policies_score" in data
    assert "risks_score" in data
    assert "controls_implemented" in data
    assert "controls_total" in data
