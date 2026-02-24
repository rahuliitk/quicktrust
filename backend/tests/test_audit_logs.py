"""Tests for the Audit Log API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_audit_logs_empty(client: AsyncClient, org_id: str, auth_headers: dict):
    response = await client.get(
        f"/api/v1/organizations/{org_id}/audit-logs",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


@pytest.mark.asyncio
async def test_audit_log_stats(client: AsyncClient, org_id: str, auth_headers: dict):
    response = await client.get(
        f"/api/v1/organizations/{org_id}/audit-logs/stats",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "by_action" in data
    assert "by_entity_type" in data


@pytest.mark.asyncio
async def test_filter_audit_logs_by_entity_type(client: AsyncClient, org_id: str, auth_headers: dict):
    response = await client.get(
        f"/api/v1/organizations/{org_id}/audit-logs",
        params={"entity_type": "control"},
        headers=auth_headers,
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_filter_audit_logs_by_action(client: AsyncClient, org_id: str, auth_headers: dict):
    response = await client.get(
        f"/api/v1/organizations/{org_id}/audit-logs",
        params={"action": "create"},
        headers=auth_headers,
    )
    assert response.status_code == 200
