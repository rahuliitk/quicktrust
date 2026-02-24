"""Tests for the Notification System API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_notifications_empty(client: AsyncClient, org_id: str, auth_headers: dict):
    response = await client.get(
        f"/api/v1/organizations/{org_id}/notifications",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


@pytest.mark.asyncio
async def test_create_notification(client: AsyncClient, org_id: str, auth_headers: dict):
    payload = {
        "title": "Test Alert",
        "message": "This is a test notification",
        "category": "monitoring_alert",
        "severity": "warning",
        "channel": "in_app",
    }
    response = await client.post(
        f"/api/v1/organizations/{org_id}/notifications",
        json=payload,
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Alert"
    assert data["severity"] == "warning"
    assert data["is_read"] is False


@pytest.mark.asyncio
async def test_notification_stats(client: AsyncClient, org_id: str, auth_headers: dict):
    response = await client.get(
        f"/api/v1/organizations/{org_id}/notifications/stats",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "unread" in data


@pytest.mark.asyncio
async def test_mark_all_read(client: AsyncClient, org_id: str, auth_headers: dict):
    response = await client.post(
        f"/api/v1/organizations/{org_id}/notifications/read-all",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert "message" in response.json()
