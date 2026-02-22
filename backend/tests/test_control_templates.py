import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_control_templates_empty(client: AsyncClient):
    resp = await client.get("/api/v1/control-templates")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_get_template_not_found(client: AsyncClient):
    resp = await client.get(
        "/api/v1/control-templates/00000000-0000-0000-0000-000000000001"
    )
    assert resp.status_code == 404
