"""Tests for the Gap Analysis API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_cross_framework_matrix(client: AsyncClient, org_id: str, auth_headers: dict):
    response = await client.get(
        f"/api/v1/organizations/{org_id}/gap-analysis/cross-framework",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_controls" in data
    assert "multi_framework_controls" in data
    assert "frameworks" in data
    assert "matrix" in data


@pytest.mark.asyncio
async def test_gap_analysis_requires_framework(client: AsyncClient, org_id: str, auth_headers: dict):
    # Using a fake UUID should return 404 or empty gap analysis
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(
        f"/api/v1/organizations/{org_id}/gap-analysis/framework/{fake_id}",
        headers=auth_headers,
    )
    # Should return 200 with zero requirements (framework not found doesn't crash)
    assert response.status_code == 200
    data = response.json()
    assert data["total_requirements"] == 0
