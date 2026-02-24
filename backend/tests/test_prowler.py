import pytest
from httpx import AsyncClient

# Test org — must be created first
TEST_ORG_ID = None
TEST_INTEGRATION_ID = None


@pytest.fixture(autouse=True)
async def setup_org(client: AsyncClient):
    global TEST_ORG_ID, TEST_INTEGRATION_ID
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Prowler Test Org", "slug": "prowler-test-org"},
    )
    TEST_ORG_ID = resp.json()["id"]

    # Create a prowler integration
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/integrations",
        json={
            "provider": "prowler",
            "name": "AWS Prowler Scanner",
            "config": {"region": "us-east-1"},
        },
    )
    TEST_INTEGRATION_ID = resp.json()["id"]


@pytest.mark.asyncio
async def test_prowler_in_providers_list(client: AsyncClient):
    """Prowler should appear in the providers list."""
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/integrations/providers"
    )
    assert resp.status_code == 200
    providers = resp.json()
    provider_names = [p["provider"] for p in providers]
    assert "prowler" in provider_names

    prowler = next(p for p in providers if p["provider"] == "prowler")
    assert "Prowler" in prowler["name"]
    assert len(prowler["collector_types"]) == 3
    assert "prowler_aws_full_scan" in prowler["collector_types"]
    assert "prowler_aws_service_scan" in prowler["collector_types"]
    assert "prowler_aws_compliance_scan" in prowler["collector_types"]


@pytest.mark.asyncio
async def test_trigger_full_scan(client: AsyncClient):
    """Trigger a full Prowler scan (falls back to mock)."""
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/prowler/scan",
        json={
            "integration_id": TEST_INTEGRATION_ID,
            "scan_type": "full",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "job_id" in data
    assert data["status"] == "completed"
    assert data["collector_type"] == "prowler_aws_full_scan"


@pytest.mark.asyncio
async def test_trigger_service_scan(client: AsyncClient):
    """Trigger a service-scoped Prowler scan."""
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/prowler/scan",
        json={
            "integration_id": TEST_INTEGRATION_ID,
            "scan_type": "service",
            "services": ["iam", "s3"],
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["collector_type"] == "prowler_aws_service_scan"


@pytest.mark.asyncio
async def test_trigger_compliance_scan(client: AsyncClient):
    """Trigger a compliance-framework Prowler scan."""
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/prowler/scan",
        json={
            "integration_id": TEST_INTEGRATION_ID,
            "scan_type": "compliance",
            "compliance_framework": "cis_1.5_aws",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["collector_type"] == "prowler_aws_compliance_scan"


@pytest.mark.asyncio
async def test_list_scan_results(client: AsyncClient):
    """List Prowler scan results after triggering a scan."""
    # First trigger a scan
    await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/prowler/scan",
        json={
            "integration_id": TEST_INTEGRATION_ID,
            "scan_type": "full",
        },
    )

    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/prowler/results"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert data["total"] >= 1
    assert len(data["items"]) >= 1

    item = data["items"][0]
    assert "job_id" in item
    assert item["status"] == "completed"
    assert item["total_findings"] > 0


@pytest.mark.asyncio
async def test_get_scan_detail(client: AsyncClient):
    """Get detailed results for a specific Prowler scan."""
    # Trigger a scan
    trigger_resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/prowler/scan",
        json={
            "integration_id": TEST_INTEGRATION_ID,
            "scan_type": "full",
        },
    )
    job_id = trigger_resp.json()["job_id"]

    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/prowler/results/{job_id}"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["job_id"] == job_id
    assert data["status"] == "completed"
    assert len(data["findings"]) > 0

    # Verify finding structure
    finding = data["findings"][0]
    assert "check_id" in finding
    assert "status" in finding
    assert "severity" in finding
    assert "service" in finding


@pytest.mark.asyncio
async def test_compliance_posture(client: AsyncClient):
    """Get compliance posture after running scans."""
    # Run a scan first
    await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/prowler/scan",
        json={
            "integration_id": TEST_INTEGRATION_ID,
            "scan_type": "full",
        },
    )

    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/prowler/compliance-posture"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "frameworks" in data
    assert "services" in data
    assert "overall_pass_rate" in data
    assert data["total_scans"] >= 1
    assert data["overall_pass_rate"] > 0


@pytest.mark.asyncio
async def test_findings_summary(client: AsyncClient):
    """Get findings summary after running a scan."""
    await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/prowler/scan",
        json={
            "integration_id": TEST_INTEGRATION_ID,
            "scan_type": "full",
        },
    )

    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/prowler/findings-summary"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] > 0
    assert data["passed"] > 0
    assert data["failed"] > 0
    assert data["pass_rate"] > 0
    assert "by_severity" in data
    assert "by_service" in data


@pytest.mark.asyncio
async def test_collector_mock_fallback():
    """Unit test that collector classes produce valid mock data."""
    from app.collectors.prowler_collectors import (
        ProwlerAwsFullScan,
        ProwlerAwsServiceScan,
        ProwlerAwsComplianceScan,
    )

    # Full scan mock
    full = ProwlerAwsFullScan()
    result = await full.collect({})
    assert result["status"] == "success"
    assert len(result["data"]["findings"]) == 15
    assert result["data"]["summary_stats"]["total"] == 15

    # Service scan mock
    service = ProwlerAwsServiceScan()
    result = await service.collect({"services": ["iam", "s3"]})
    assert result["status"] == "success"
    assert len(result["data"]["findings"]) == 8

    # Compliance scan mock
    compliance = ProwlerAwsComplianceScan()
    result = await compliance.collect({"compliance_framework": "cis_1.5_aws"})
    assert result["status"] == "success"
    assert len(result["data"]["findings"]) == 10


@pytest.mark.asyncio
async def test_collector_via_integration_api(client: AsyncClient):
    """Trigger collection via the standard integrations API."""
    resp = await client.post(
        f"/api/v1/organizations/{TEST_ORG_ID}/integrations/{TEST_INTEGRATION_ID}/collect",
        json={"collector_type": "prowler_aws_full_scan"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "completed"
    assert data["collector_type"] == "prowler_aws_full_scan"
    assert data["result_data"]["status"] == "success"


@pytest.mark.asyncio
async def test_findings_summary_empty(client: AsyncClient):
    """Findings summary returns zeros when no scans exist."""
    # Create a fresh org with no scans
    org_resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Empty Prowler Org", "slug": "empty-prowler-org"},
    )
    empty_org_id = org_resp.json()["id"]

    resp = await client.get(
        f"/api/v1/organizations/{empty_org_id}/prowler/findings-summary"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0
    assert data["pass_rate"] == 0


@pytest.mark.asyncio
async def test_scan_detail_not_found(client: AsyncClient):
    """Non-existent scan returns 404."""
    import uuid
    fake_id = str(uuid.uuid4())
    resp = await client.get(
        f"/api/v1/organizations/{TEST_ORG_ID}/prowler/results/{fake_id}"
    )
    assert resp.status_code == 404
