"""Tests for the Tenant Management API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_tenants(client: AsyncClient, auth_headers: dict):
    response = await client.get(
        "/api/v1/tenants",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data


@pytest.mark.asyncio
async def test_provision_tenant(client: AsyncClient, auth_headers: dict):
    payload = {
        "name": "Test Corp",
        "industry": "technology",
        "company_size": "50-200",
    }
    response = await client.post(
        "/api/v1/tenants/provision",
        json=payload,
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert "organization" in data
    assert data["organization"]["name"] == "Test Corp"


@pytest.mark.asyncio
async def test_provision_duplicate_tenant_fails(client: AsyncClient, auth_headers: dict):
    payload = {"name": "Duplicate Test"}
    # First creation
    resp1 = await client.post("/api/v1/tenants/provision", json=payload, headers=auth_headers)
    assert resp1.status_code == 201

    # Duplicate
    resp2 = await client.post("/api/v1/tenants/provision", json=payload, headers=auth_headers)
    assert resp2.status_code == 409


@pytest.mark.asyncio
async def test_tenant_isolation_check(client: AsyncClient, org_id: str, auth_headers: dict):
    response = await client.get(
        f"/api/v1/tenants/{org_id}/isolation-check",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["org_id"] == org_id
    assert "tables_checked" in data
    assert "all_isolated" in data
