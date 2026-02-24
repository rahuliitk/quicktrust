"""Tests for the Auditor Marketplace API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_search_marketplace_empty(client: AsyncClient, auth_headers: dict):
    response = await client.get(
        "/api/v1/auditor-marketplace",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


@pytest.mark.asyncio
async def test_search_marketplace_with_filters(client: AsyncClient, auth_headers: dict):
    response = await client.get(
        "/api/v1/auditor-marketplace",
        params={"specialization": "SOC 2", "verified_only": True},
        headers=auth_headers,
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_register_auditor(client: AsyncClient, auth_headers: dict):
    payload = {
        "firm_name": "Test Audit Firm",
        "bio": "Experienced compliance auditor",
        "credentials": ["CPA", "CISA"],
        "specializations": ["SOC 2", "ISO 27001"],
        "years_experience": 10,
        "location": "New York, NY",
        "hourly_rate": 250.0,
    }
    response = await client.post(
        "/api/v1/auditor-marketplace/register",
        json=payload,
        headers=auth_headers,
    )
    # May be 201 or 400 if profile already exists
    assert response.status_code in (201, 400)


@pytest.mark.asyncio
async def test_get_my_profile(client: AsyncClient, auth_headers: dict):
    response = await client.get(
        "/api/v1/auditor-marketplace/me/profile",
        headers=auth_headers,
    )
    assert response.status_code == 200
