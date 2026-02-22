import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_frameworks_empty(client: AsyncClient):
    resp = await client.get("/api/v1/frameworks")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_get_framework_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/frameworks/00000000-0000-0000-0000-000000000001")
    assert resp.status_code == 404
