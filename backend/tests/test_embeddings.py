"""Tests for the Embeddings / Semantic Search API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_search_empty(client: AsyncClient, org_id: str, auth_headers: dict):
    payload = {"query": "access control", "entity_type": "control"}
    response = await client.post(
        f"/api/v1/organizations/{org_id}/embeddings/search",
        json=payload,
        headers=auth_headers,
    )
    assert response.status_code == 200
    # Returns empty list when no embeddings exist or model not available
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_index_entities(client: AsyncClient, org_id: str, auth_headers: dict):
    response = await client.post(
        f"/api/v1/organizations/{org_id}/embeddings/index/control",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_index_invalid_entity_type(client: AsyncClient, org_id: str, auth_headers: dict):
    response = await client.post(
        f"/api/v1/organizations/{org_id}/embeddings/index/invalid_type",
        headers=auth_headers,
    )
    assert response.status_code == 400
