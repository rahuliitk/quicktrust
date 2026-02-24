"""Pydantic schemas for Prowler security scanner integration."""
from pydantic import BaseModel, Field


class ProwlerScanTrigger(BaseModel):
    integration_id: str
    scan_type: str = Field(default="full", description="full | service | compliance")
    services: list[str] | None = Field(default=None, description="Services to scan (for service scan type)")
    compliance_framework: str | None = Field(default=None, description="Framework ID (for compliance scan type)")


class ProwlerFinding(BaseModel):
    check_id: str = ""
    check_title: str = ""
    status: str = ""
    severity: str = ""
    service: str = ""
    region: str = ""
    resource_id: str = ""
    resource_arn: str = ""
    status_extended: str = ""
    risk: str = ""
    remediation: str = ""
    compliance: dict = Field(default_factory=dict)


class ProwlerScanResultResponse(BaseModel):
    job_id: str
    status: str
    scan_type: str | None = None
    cloud_provider: str | None = None
    total_findings: int = 0
    passed: int = 0
    failed: int = 0
    pass_rate: float = 0.0
    created_at: str | None = None
    findings: list[ProwlerFinding] = Field(default_factory=list)


class ComplianceFrameworkPosture(BaseModel):
    framework: str
    total_checks: int = 0
    passed: int = 0
    failed: int = 0
    pass_rate: float = 0.0


class ServicePosture(BaseModel):
    service: str
    total_checks: int = 0
    passed: int = 0
    failed: int = 0
    pass_rate: float = 0.0


class ProwlerCompliancePosture(BaseModel):
    frameworks: list[ComplianceFrameworkPosture] = Field(default_factory=list)
    services: list[ServicePosture] = Field(default_factory=list)
    overall_pass_rate: float = 0.0
    total_scans: int = 0
    last_scan_at: str | None = None


class ProwlerFindingSummary(BaseModel):
    total: int = 0
    passed: int = 0
    failed: int = 0
    pass_rate: float = 0.0
    by_severity: dict[str, int] = Field(default_factory=dict)
    by_service: dict[str, int] = Field(default_factory=dict)
    critical_count: int = 0
    high_count: int = 0
    last_scan_at: str | None = None
