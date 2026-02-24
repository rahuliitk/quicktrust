import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.dependencies import get_current_user
from app.main import app
from app.models.user import User
from tests.conftest import make_test_user_with_role

# Test org — must be created first
TEST_ORG_ID = None


def _override_user_factory(role: str):
    """Return an async callable that provides a User with the given role."""
    async def _override():
        return make_test_user_with_role(role)
    return _override


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "RBAC Test Org", "slug": "rbac-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]


@pytest.fixture
async def admin_client():
    """Client authenticated as admin role."""
    app.dependency_overrides[get_current_user] = _override_user_factory("admin")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    # Restore super_admin override
    from tests.conftest import override_get_current_user
    app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.fixture
async def employee_client():
    """Client authenticated as employee role."""
    app.dependency_overrides[get_current_user] = _override_user_factory("employee")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    from tests.conftest import override_get_current_user
    app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.fixture
async def compliance_manager_client():
    """Client authenticated as compliance_manager role."""
    app.dependency_overrides[get_current_user] = _override_user_factory("compliance_manager")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    from tests.conftest import override_get_current_user
    app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.fixture
async def auditor_external_client():
    """Client authenticated as auditor_external role."""
    app.dependency_overrides[get_current_user] = _override_user_factory("auditor_external")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    from tests.conftest import override_get_current_user
    app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.mark.asyncio
async def test_admin_can_access_settings(admin_client: AsyncClient):
    """Admin role should be able to read organization details (settings proxy)."""
    resp = await admin_client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/audits/readiness"
    )
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_employee_cannot_access_settings(employee_client: AsyncClient):
    """Employee role should be denied access to compliance-level endpoints."""
    resp = await employee_client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/controls",
        json={
            "title": "Unauthorized Control",
            "description": "Employee trying to create a control",
            "status": "draft",
            "automation_level": "manual",
        },
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_compliance_manager_can_create_control(compliance_manager_client: AsyncClient):
    """Compliance manager should be able to create controls."""
    resp = await compliance_manager_client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/controls",
        json={
            "title": "Compliance Manager Control",
            "description": "Control created by compliance manager",
            "status": "draft",
            "automation_level": "manual",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["title"] == "Compliance Manager Control"


@pytest.mark.asyncio
async def test_auditor_external_read_only(auditor_external_client: AsyncClient):
    """External auditor should not be able to create controls (write operations)."""
    resp = await auditor_external_client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/controls",
        json={
            "title": "External Auditor Control",
            "description": "Auditor trying to create a control",
            "status": "draft",
            "automation_level": "manual",
        },
    )
    assert resp.status_code == 403

    # External auditors should also be denied access to internal-only list endpoints
    list_resp = await auditor_external_client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/controls"
    )
    assert list_resp.status_code == 403
