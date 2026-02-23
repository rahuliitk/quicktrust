"""Base collector interface and registry."""
from abc import ABC, abstractmethod
from typing import Any

COLLECTOR_REGISTRY: dict[str, "BaseCollector"] = {}


def register_collector(collector_type: str):
    """Decorator to register a collector class in the global registry."""
    def decorator(cls):
        COLLECTOR_REGISTRY[collector_type] = cls()
        return cls
    return decorator


class BaseCollector(ABC):
    """Abstract base class for evidence collectors."""

    @abstractmethod
    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        """
        Run the collection and return result data.

        Returns a dict with:
          - status: "success" | "failure"
          - data: collected evidence payload
          - summary: human-readable summary
        """
        ...
