"""AWS mock collectors for evidence auto-collection."""
from datetime import datetime, timezone
from typing import Any

from app.collectors.base import BaseCollector, register_collector


@register_collector("aws_iam_mfa_report")
class AwsIamMfaReport(BaseCollector):
    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "IAM MFA compliance report collected",
            "data": {
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "total_users": 45,
                "mfa_enabled": 43,
                "mfa_disabled": 2,
                "compliance_rate": 95.6,
                "non_compliant_users": [
                    {"username": "service-account-legacy", "last_activity": "2025-12-01"},
                    {"username": "temp-contractor-22", "last_activity": "2026-01-15"},
                ],
            },
        }


@register_collector("aws_cloudtrail_status")
class AwsCloudTrailStatus(BaseCollector):
    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "CloudTrail configuration verified",
            "data": {
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "trails": [
                    {
                        "name": "organization-trail",
                        "is_multi_region": True,
                        "is_logging": True,
                        "log_file_validation": True,
                        "s3_bucket": "company-cloudtrail-logs",
                        "kms_key_id": "arn:aws:kms:us-east-1:123456789:key/example",
                    }
                ],
                "compliant": True,
            },
        }


@register_collector("aws_encryption_at_rest")
class AwsEncryptionAtRest(BaseCollector):
    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "Encryption at rest status collected",
            "data": {
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "services": {
                    "s3": {"encrypted_buckets": 12, "total_buckets": 12, "compliant": True},
                    "rds": {"encrypted_instances": 5, "total_instances": 5, "compliant": True},
                    "ebs": {"encrypted_volumes": 28, "total_volumes": 30, "compliant": False},
                    "dynamodb": {"encrypted_tables": 8, "total_tables": 8, "compliant": True},
                },
                "overall_compliance": 96.4,
            },
        }
