"""State definitions for the monitoring daemon agent."""
from typing import TypedDict


class MonitoringDaemonState(TypedDict, total=False):
    # Input
    org_id: str
    agent_run_id: str

    # Intermediate
    rules: list[dict]
    check_results: list[dict]
    drift_detections: list[dict]
    alerts_generated: list[dict]

    # Output
    summary: dict
    error: str | None
