"""Prowler security scanner collectors for cloud security posture assessment.

Each collector attempts to run the Prowler CLI tool. If Prowler is not
installed or the scan fails, the collector falls back to mock data so that
the application works without live cloud connectivity.
"""
import asyncio
import json
import logging
import os
import tempfile
from datetime import datetime, timezone
from typing import Any

from app.collectors.base import BaseCollector, register_collector
from app.config import get_settings

logger = logging.getLogger(__name__)


async def _run_prowler_scan(
    cloud_provider: str,
    credentials: dict | None,
    scan_scope: dict | None = None,
    output_dir: str | None = None,
) -> list[dict]:
    """Run the prowler CLI as an async subprocess and parse JSON output."""
    settings = get_settings()
    output_dir = output_dir or settings.PROWLER_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    cmd = ["prowler", cloud_provider, "-M", "json", "-o", output_dir, "-F", "prowler-output"]

    if scan_scope:
        if scan_scope.get("services"):
            cmd.extend(["-s", ",".join(scan_scope["services"])])
        if scan_scope.get("compliance_framework"):
            cmd.extend(["--compliance", scan_scope["compliance_framework"]])

    env = os.environ.copy()
    if credentials:
        if credentials.get("aws_access_key_id"):
            env["AWS_ACCESS_KEY_ID"] = credentials["aws_access_key_id"]
        if credentials.get("aws_secret_access_key"):
            env["AWS_SECRET_ACCESS_KEY"] = credentials["aws_secret_access_key"]
        if credentials.get("aws_session_token"):
            env["AWS_SESSION_TOKEN"] = credentials["aws_session_token"]
        if credentials.get("aws_region"):
            env["AWS_DEFAULT_REGION"] = credentials["aws_region"]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
    )
    _, stderr = await asyncio.wait_for(
        proc.communicate(), timeout=settings.PROWLER_TIMEOUT_SECONDS
    )

    if proc.returncode not in (0, 3):  # 3 = findings found (non-zero but expected)
        raise RuntimeError(f"Prowler exited with code {proc.returncode}: {stderr.decode()[:500]}")

    output_file = os.path.join(output_dir, "prowler-output.json")
    if not os.path.exists(output_file):
        raise FileNotFoundError(f"Prowler output not found at {output_file}")

    with open(output_file) as f:
        return json.load(f)


def _normalize_findings(raw_findings: list[dict]) -> list[dict]:
    """Normalize Prowler JSON output keys to a consistent format."""
    normalized = []
    for finding in raw_findings:
        normalized.append({
            "check_id": finding.get("CheckID") or finding.get("check_id", ""),
            "check_title": finding.get("CheckTitle") or finding.get("check_title", ""),
            "status": finding.get("Status") or finding.get("status", ""),
            "severity": finding.get("Severity") or finding.get("severity", ""),
            "service": finding.get("ServiceName") or finding.get("service", ""),
            "region": finding.get("Region") or finding.get("region", ""),
            "resource_id": finding.get("ResourceId") or finding.get("resource_id", ""),
            "resource_arn": finding.get("ResourceArn") or finding.get("resource_arn", ""),
            "status_extended": finding.get("StatusExtended") or finding.get("status_extended", ""),
            "risk": finding.get("Risk") or finding.get("risk", ""),
            "remediation": finding.get("Remediation", {}).get("Recommendation", {}).get("Text", "")
            if isinstance(finding.get("Remediation"), dict)
            else finding.get("remediation", ""),
            "compliance": finding.get("Compliance", {}) if isinstance(finding.get("Compliance"), dict) else {},
        })
    return normalized


def _compute_summary_stats(findings: list[dict]) -> dict:
    """Aggregate summary statistics from normalized findings."""
    total = len(findings)
    passed = sum(1 for f in findings if f["status"].upper() == "PASS")
    failed = sum(1 for f in findings if f["status"].upper() == "FAIL")
    pass_rate = round((passed / total * 100), 1) if total > 0 else 0.0

    by_severity: dict[str, int] = {}
    by_service: dict[str, int] = {}
    for f in findings:
        sev = f.get("severity", "unknown").lower()
        svc = f.get("service", "unknown")
        if f["status"].upper() == "FAIL":
            by_severity[sev] = by_severity.get(sev, 0) + 1
            by_service[svc] = by_service.get(svc, 0) + 1

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate,
        "by_severity": by_severity,
        "by_service": by_service,
    }


# ---------------------------------------------------------------------------
# Full AWS Scan
# ---------------------------------------------------------------------------

@register_collector("prowler_aws_full_scan")
class ProwlerAwsFullScan(BaseCollector):
    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        try:
            raw = await _run_prowler_scan("aws", credentials)
            findings = _normalize_findings(raw)
            summary = _compute_summary_stats(findings)
            logger.info("Prowler full AWS scan completed (%d findings)", len(findings))
            return {
                "status": "success",
                "summary": f"Prowler full AWS scan: {summary['total']} checks, {summary['pass_rate']}% pass rate",
                "data": {
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "scan_type": "full",
                    "cloud_provider": "aws",
                    "findings": findings,
                    "summary_stats": summary,
                },
            }
        except Exception as exc:
            logger.warning("Prowler full AWS scan failed, using mock data: %s", exc)
            return self._mock_response()

    @staticmethod
    def _mock_response() -> dict[str, Any]:
        findings = [
            {"check_id": "iam_root_mfa_enabled", "check_title": "Ensure MFA is enabled for the root account", "status": "FAIL", "severity": "critical", "service": "IAM", "region": "us-east-1", "resource_id": "root", "resource_arn": "arn:aws:iam::123456789012:root", "status_extended": "Root account does not have MFA enabled", "risk": "Root account compromise", "remediation": "Enable MFA on the root account", "compliance": {"CIS": ["1.5"], "SOC2": ["CC6.1"]}},
            {"check_id": "iam_password_policy_uppercase", "check_title": "Ensure IAM password policy requires uppercase", "status": "PASS", "severity": "medium", "service": "IAM", "region": "us-east-1", "resource_id": "password_policy", "resource_arn": "", "status_extended": "Password policy requires uppercase letters", "risk": "", "remediation": "", "compliance": {"CIS": ["1.8"]}},
            {"check_id": "s3_bucket_public_access", "check_title": "Ensure S3 buckets block public access", "status": "FAIL", "severity": "high", "service": "S3", "region": "us-east-1", "resource_id": "my-public-bucket", "resource_arn": "arn:aws:s3:::my-public-bucket", "status_extended": "Bucket my-public-bucket has public access enabled", "risk": "Data exposure", "remediation": "Enable S3 Block Public Access", "compliance": {"CIS": ["2.1.2"], "PCI": ["2.2"]}},
            {"check_id": "s3_bucket_encryption", "check_title": "Ensure S3 bucket encryption is enabled", "status": "PASS", "severity": "medium", "service": "S3", "region": "us-east-1", "resource_id": "encrypted-bucket", "resource_arn": "arn:aws:s3:::encrypted-bucket", "status_extended": "Bucket encryption is enabled with AES-256", "risk": "", "remediation": "", "compliance": {"CIS": ["2.1.1"]}},
            {"check_id": "cloudtrail_multi_region", "check_title": "Ensure CloudTrail is enabled in all regions", "status": "PASS", "severity": "high", "service": "CloudTrail", "region": "us-east-1", "resource_id": "org-trail", "resource_arn": "arn:aws:cloudtrail:us-east-1:123456789012:trail/org-trail", "status_extended": "Multi-region trail is active and logging", "risk": "", "remediation": "", "compliance": {"CIS": ["3.1"], "SOC2": ["CC7.2"]}},
            {"check_id": "cloudtrail_log_file_validation", "check_title": "Ensure CloudTrail log file validation is enabled", "status": "PASS", "severity": "medium", "service": "CloudTrail", "region": "us-east-1", "resource_id": "org-trail", "resource_arn": "arn:aws:cloudtrail:us-east-1:123456789012:trail/org-trail", "status_extended": "Log file validation is enabled", "risk": "", "remediation": "", "compliance": {"CIS": ["3.2"]}},
            {"check_id": "ec2_security_group_open_ssh", "check_title": "Ensure no security groups allow SSH from 0.0.0.0/0", "status": "FAIL", "severity": "high", "service": "EC2", "region": "us-east-1", "resource_id": "sg-0abc123def", "resource_arn": "arn:aws:ec2:us-east-1:123456789012:security-group/sg-0abc123def", "status_extended": "Security group sg-0abc123def allows SSH from 0.0.0.0/0", "risk": "Unauthorized SSH access", "remediation": "Restrict SSH access to known IP ranges", "compliance": {"CIS": ["5.2"], "PCI": ["1.3.4"]}},
            {"check_id": "ec2_ebs_encryption", "check_title": "Ensure EBS volume encryption is enabled by default", "status": "PASS", "severity": "medium", "service": "EC2", "region": "us-east-1", "resource_id": "ebs-default-encryption", "resource_arn": "", "status_extended": "EBS default encryption is enabled", "risk": "", "remediation": "", "compliance": {"CIS": ["2.2.1"]}},
            {"check_id": "rds_instance_encryption", "check_title": "Ensure RDS instances have encryption enabled", "status": "PASS", "severity": "high", "service": "RDS", "region": "us-east-1", "resource_id": "prod-db", "resource_arn": "arn:aws:rds:us-east-1:123456789012:db:prod-db", "status_extended": "RDS instance prod-db is encrypted", "risk": "", "remediation": "", "compliance": {"CIS": ["2.3.1"]}},
            {"check_id": "rds_instance_public_access", "check_title": "Ensure RDS instances are not publicly accessible", "status": "FAIL", "severity": "critical", "service": "RDS", "region": "us-east-1", "resource_id": "staging-db", "resource_arn": "arn:aws:rds:us-east-1:123456789012:db:staging-db", "status_extended": "RDS instance staging-db is publicly accessible", "risk": "Database exposure", "remediation": "Disable public accessibility on the RDS instance", "compliance": {"CIS": ["2.3.2"], "HIPAA": ["164.312(e)(1)"]}},
            {"check_id": "iam_user_console_access_mfa", "check_title": "Ensure MFA is enabled for all IAM users with console access", "status": "FAIL", "severity": "high", "service": "IAM", "region": "us-east-1", "resource_id": "dev-user-legacy", "resource_arn": "arn:aws:iam::123456789012:user/dev-user-legacy", "status_extended": "User dev-user-legacy has console access without MFA", "risk": "Account compromise", "remediation": "Enable MFA for the user", "compliance": {"CIS": ["1.10"], "SOC2": ["CC6.1"]}},
            {"check_id": "s3_bucket_versioning", "check_title": "Ensure S3 bucket versioning is enabled", "status": "PASS", "severity": "low", "service": "S3", "region": "us-east-1", "resource_id": "versioned-bucket", "resource_arn": "arn:aws:s3:::versioned-bucket", "status_extended": "Bucket versioning is enabled", "risk": "", "remediation": "", "compliance": {}},
            {"check_id": "cloudtrail_kms_encryption", "check_title": "Ensure CloudTrail logs are encrypted with KMS", "status": "PASS", "severity": "medium", "service": "CloudTrail", "region": "us-east-1", "resource_id": "org-trail", "resource_arn": "arn:aws:cloudtrail:us-east-1:123456789012:trail/org-trail", "status_extended": "CloudTrail logs are encrypted with KMS", "risk": "", "remediation": "", "compliance": {"CIS": ["3.7"]}},
            {"check_id": "ec2_instance_imdsv2", "check_title": "Ensure EC2 instances use IMDSv2", "status": "FAIL", "severity": "medium", "service": "EC2", "region": "us-east-1", "resource_id": "i-0abc123def456", "resource_arn": "arn:aws:ec2:us-east-1:123456789012:instance/i-0abc123def456", "status_extended": "Instance i-0abc123def456 does not enforce IMDSv2", "risk": "SSRF attacks can extract credentials", "remediation": "Set HttpTokens to required on the instance", "compliance": {"CIS": ["5.6"]}},
            {"check_id": "iam_access_key_rotation", "check_title": "Ensure access keys are rotated within 90 days", "status": "PASS", "severity": "medium", "service": "IAM", "region": "us-east-1", "resource_id": "admin-user", "resource_arn": "arn:aws:iam::123456789012:user/admin-user", "status_extended": "Access key was rotated 45 days ago", "risk": "", "remediation": "", "compliance": {"CIS": ["1.14"]}},
        ]
        summary = _compute_summary_stats(findings)
        return {
            "status": "success",
            "summary": f"Prowler full AWS scan: {summary['total']} checks, {summary['pass_rate']}% pass rate (mock)",
            "data": {
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "scan_type": "full",
                "cloud_provider": "aws",
                "findings": findings,
                "summary_stats": summary,
            },
        }


# ---------------------------------------------------------------------------
# Service-scoped AWS Scan
# ---------------------------------------------------------------------------

@register_collector("prowler_aws_service_scan")
class ProwlerAwsServiceScan(BaseCollector):
    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        services = config.get("services", ["iam", "s3"])
        try:
            raw = await _run_prowler_scan("aws", credentials, scan_scope={"services": services})
            findings = _normalize_findings(raw)
            summary = _compute_summary_stats(findings)
            logger.info("Prowler service scan (%s) completed (%d findings)", services, len(findings))
            return {
                "status": "success",
                "summary": f"Prowler service scan ({', '.join(services)}): {summary['total']} checks, {summary['pass_rate']}% pass rate",
                "data": {
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "scan_type": "service",
                    "cloud_provider": "aws",
                    "services_scanned": services,
                    "findings": findings,
                    "summary_stats": summary,
                },
            }
        except Exception as exc:
            logger.warning("Prowler service scan failed, using mock data: %s", exc)
            return self._mock_response(services)

    @staticmethod
    def _mock_response(services: list[str] | None = None) -> dict[str, Any]:
        services = services or ["iam", "s3"]
        findings = [
            {"check_id": "iam_root_mfa_enabled", "check_title": "Ensure MFA is enabled for the root account", "status": "FAIL", "severity": "critical", "service": "IAM", "region": "us-east-1", "resource_id": "root", "resource_arn": "arn:aws:iam::123456789012:root", "status_extended": "Root account does not have MFA enabled", "risk": "Root account compromise", "remediation": "Enable MFA on the root account", "compliance": {"CIS": ["1.5"]}},
            {"check_id": "iam_password_policy_uppercase", "check_title": "Ensure IAM password policy requires uppercase", "status": "PASS", "severity": "medium", "service": "IAM", "region": "us-east-1", "resource_id": "password_policy", "resource_arn": "", "status_extended": "Password policy requires uppercase", "risk": "", "remediation": "", "compliance": {"CIS": ["1.8"]}},
            {"check_id": "s3_bucket_public_access", "check_title": "Ensure S3 buckets block public access", "status": "FAIL", "severity": "high", "service": "S3", "region": "us-east-1", "resource_id": "my-public-bucket", "resource_arn": "arn:aws:s3:::my-public-bucket", "status_extended": "Bucket has public access", "risk": "Data exposure", "remediation": "Enable Block Public Access", "compliance": {"CIS": ["2.1.2"]}},
            {"check_id": "s3_bucket_encryption", "check_title": "Ensure S3 bucket encryption is enabled", "status": "PASS", "severity": "medium", "service": "S3", "region": "us-east-1", "resource_id": "encrypted-bucket", "resource_arn": "arn:aws:s3:::encrypted-bucket", "status_extended": "Encryption enabled", "risk": "", "remediation": "", "compliance": {"CIS": ["2.1.1"]}},
            {"check_id": "iam_user_console_access_mfa", "check_title": "Ensure MFA for console users", "status": "FAIL", "severity": "high", "service": "IAM", "region": "us-east-1", "resource_id": "dev-user", "resource_arn": "arn:aws:iam::123456789012:user/dev-user", "status_extended": "User lacks MFA", "risk": "Account compromise", "remediation": "Enable MFA", "compliance": {"CIS": ["1.10"]}},
            {"check_id": "s3_bucket_versioning", "check_title": "Ensure S3 bucket versioning is enabled", "status": "PASS", "severity": "low", "service": "S3", "region": "us-east-1", "resource_id": "versioned-bucket", "resource_arn": "arn:aws:s3:::versioned-bucket", "status_extended": "Versioning enabled", "risk": "", "remediation": "", "compliance": {}},
            {"check_id": "iam_access_key_rotation", "check_title": "Ensure access keys rotated within 90 days", "status": "PASS", "severity": "medium", "service": "IAM", "region": "us-east-1", "resource_id": "admin-user", "resource_arn": "arn:aws:iam::123456789012:user/admin-user", "status_extended": "Rotated 30 days ago", "risk": "", "remediation": "", "compliance": {"CIS": ["1.14"]}},
            {"check_id": "s3_bucket_logging", "check_title": "Ensure S3 bucket logging is enabled", "status": "FAIL", "severity": "medium", "service": "S3", "region": "us-east-1", "resource_id": "unlogged-bucket", "resource_arn": "arn:aws:s3:::unlogged-bucket", "status_extended": "Logging not enabled", "risk": "Audit trail gap", "remediation": "Enable server access logging", "compliance": {"CIS": ["2.6"]}},
        ]
        summary = _compute_summary_stats(findings)
        return {
            "status": "success",
            "summary": f"Prowler service scan ({', '.join(services)}): {summary['total']} checks, {summary['pass_rate']}% pass rate (mock)",
            "data": {
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "scan_type": "service",
                "cloud_provider": "aws",
                "services_scanned": services,
                "findings": findings,
                "summary_stats": summary,
            },
        }


# ---------------------------------------------------------------------------
# Compliance Framework Scan
# ---------------------------------------------------------------------------

@register_collector("prowler_aws_compliance_scan")
class ProwlerAwsComplianceScan(BaseCollector):
    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        framework = config.get("compliance_framework", "cis_1.5_aws")
        try:
            raw = await _run_prowler_scan("aws", credentials, scan_scope={"compliance_framework": framework})
            findings = _normalize_findings(raw)
            summary = _compute_summary_stats(findings)
            logger.info("Prowler compliance scan (%s) completed (%d findings)", framework, len(findings))
            return {
                "status": "success",
                "summary": f"Prowler compliance scan ({framework}): {summary['total']} checks, {summary['pass_rate']}% pass rate",
                "data": {
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "scan_type": "compliance",
                    "cloud_provider": "aws",
                    "compliance_framework": framework,
                    "findings": findings,
                    "summary_stats": summary,
                },
            }
        except Exception as exc:
            logger.warning("Prowler compliance scan failed, using mock data: %s", exc)
            return self._mock_response(framework)

    @staticmethod
    def _mock_response(framework: str = "cis_1.5_aws") -> dict[str, Any]:
        findings = [
            {"check_id": "iam_root_mfa_enabled", "check_title": "Ensure MFA is enabled for the root account", "status": "FAIL", "severity": "critical", "service": "IAM", "region": "us-east-1", "resource_id": "root", "resource_arn": "arn:aws:iam::123456789012:root", "status_extended": "Root account MFA not enabled", "risk": "Root compromise", "remediation": "Enable root MFA", "compliance": {"CIS": ["1.5"]}},
            {"check_id": "iam_password_policy_length", "check_title": "Ensure password policy requires minimum length of 14", "status": "PASS", "severity": "medium", "service": "IAM", "region": "us-east-1", "resource_id": "password_policy", "resource_arn": "", "status_extended": "Min length is 14", "risk": "", "remediation": "", "compliance": {"CIS": ["1.9"]}},
            {"check_id": "cloudtrail_multi_region", "check_title": "Ensure CloudTrail is enabled in all regions", "status": "PASS", "severity": "high", "service": "CloudTrail", "region": "us-east-1", "resource_id": "org-trail", "resource_arn": "arn:aws:cloudtrail:us-east-1:123456789012:trail/org-trail", "status_extended": "Multi-region enabled", "risk": "", "remediation": "", "compliance": {"CIS": ["3.1"]}},
            {"check_id": "cloudtrail_log_file_validation", "check_title": "Ensure CloudTrail log file validation is enabled", "status": "PASS", "severity": "medium", "service": "CloudTrail", "region": "us-east-1", "resource_id": "org-trail", "resource_arn": "arn:aws:cloudtrail:us-east-1:123456789012:trail/org-trail", "status_extended": "Validation enabled", "risk": "", "remediation": "", "compliance": {"CIS": ["3.2"]}},
            {"check_id": "s3_bucket_public_access", "check_title": "Ensure S3 buckets block public access", "status": "FAIL", "severity": "high", "service": "S3", "region": "us-east-1", "resource_id": "public-bucket", "resource_arn": "arn:aws:s3:::public-bucket", "status_extended": "Public access not blocked", "risk": "Data leak", "remediation": "Enable Block Public Access", "compliance": {"CIS": ["2.1.2"]}},
            {"check_id": "ec2_security_group_open_ssh", "check_title": "Ensure no SGs allow SSH from 0.0.0.0/0", "status": "FAIL", "severity": "high", "service": "EC2", "region": "us-east-1", "resource_id": "sg-0abc123", "resource_arn": "arn:aws:ec2:us-east-1:123456789012:security-group/sg-0abc123", "status_extended": "SSH open to world", "risk": "Unauthorized access", "remediation": "Restrict SSH to known IPs", "compliance": {"CIS": ["5.2"]}},
            {"check_id": "rds_instance_encryption", "check_title": "Ensure RDS encryption is enabled", "status": "PASS", "severity": "high", "service": "RDS", "region": "us-east-1", "resource_id": "prod-db", "resource_arn": "arn:aws:rds:us-east-1:123456789012:db:prod-db", "status_extended": "Encrypted", "risk": "", "remediation": "", "compliance": {"CIS": ["2.3.1"]}},
            {"check_id": "ec2_ebs_encryption", "check_title": "Ensure EBS default encryption is enabled", "status": "PASS", "severity": "medium", "service": "EC2", "region": "us-east-1", "resource_id": "ebs-default", "resource_arn": "", "status_extended": "Default encryption enabled", "risk": "", "remediation": "", "compliance": {"CIS": ["2.2.1"]}},
            {"check_id": "iam_user_console_access_mfa", "check_title": "Ensure MFA for console users", "status": "FAIL", "severity": "high", "service": "IAM", "region": "us-east-1", "resource_id": "legacy-user", "resource_arn": "arn:aws:iam::123456789012:user/legacy-user", "status_extended": "Console access without MFA", "risk": "Account takeover", "remediation": "Enable MFA", "compliance": {"CIS": ["1.10"]}},
            {"check_id": "cloudtrail_kms_encryption", "check_title": "Ensure CloudTrail encrypted with KMS", "status": "PASS", "severity": "medium", "service": "CloudTrail", "region": "us-east-1", "resource_id": "org-trail", "resource_arn": "arn:aws:cloudtrail:us-east-1:123456789012:trail/org-trail", "status_extended": "KMS encryption enabled", "risk": "", "remediation": "", "compliance": {"CIS": ["3.7"]}},
        ]
        summary = _compute_summary_stats(findings)
        return {
            "status": "success",
            "summary": f"Prowler compliance scan ({framework}): {summary['total']} checks, {summary['pass_rate']}% pass rate (mock)",
            "data": {
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "scan_type": "compliance",
                "cloud_provider": "aws",
                "compliance_framework": framework,
                "findings": findings,
                "summary_stats": summary,
            },
        }
