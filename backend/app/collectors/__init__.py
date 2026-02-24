"""Evidence collectors package."""
from app.collectors.base import COLLECTOR_REGISTRY, BaseCollector

# Import collectors so they register themselves
import app.collectors.aws_collectors  # noqa: F401
import app.collectors.github_collectors  # noqa: F401
import app.collectors.okta_collectors  # noqa: F401
import app.collectors.prowler_collectors  # noqa: F401

__all__ = ["COLLECTOR_REGISTRY", "BaseCollector"]
