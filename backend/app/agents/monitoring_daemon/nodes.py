"""Node functions for the monitoring daemon LangGraph."""
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.monitoring_daemon.state import MonitoringDaemonState
from app.models.monitoring import MonitorRule, MonitorAlert
from app.services import monitoring_service


async def load_active_rules(
    state: MonitoringDaemonState, db: AsyncSession
) -> dict:
    """Load all active MonitorRule records from the database."""
    org_id = state["org_id"]

    result = await db.execute(
        select(MonitorRule).where(
            MonitorRule.org_id == org_id,
            MonitorRule.is_active == True,
        )
    )
    rules = result.scalars().all()

    if not rules:
        return {"error": f"No active monitoring rules found for organization {org_id}"}

    rules_data = []
    for r in rules:
        rules_data.append({
            "id": str(r.id),
            "title": r.title,
            "description": r.description or "",
            "check_type": r.check_type,
            "schedule": r.schedule,
            "config": r.config or {},
            "last_checked_at": str(r.last_checked_at) if r.last_checked_at else None,
            "last_result": r.last_result,
            "control_id": str(r.control_id) if r.control_id else None,
        })

    return {"rules": rules_data}


async def run_all_checks(
    state: MonitoringDaemonState, db: AsyncSession
) -> dict:
    """Call monitoring_service.run_checks() for each active rule."""
    rules = state["rules"]
    org_id = state["org_id"]
    check_results = []

    for rule in rules:
        rule_id = rule["id"]
        try:
            alerts = await monitoring_service.run_checks(db, org_id, rule_id)
            check_results.append({
                "rule_id": rule_id,
                "rule_title": rule["title"],
                "check_type": rule["check_type"],
                "status": "fail" if alerts else "pass",
                "alerts_count": len(alerts),
                "alert_ids": [str(a.id) for a in alerts],
            })
        except Exception as e:
            check_results.append({
                "rule_id": rule_id,
                "rule_title": rule["title"],
                "check_type": rule["check_type"],
                "status": "error",
                "alerts_count": 0,
                "alert_ids": [],
                "error": str(e),
            })

    return {"check_results": check_results}


async def detect_drift(
    state: MonitoringDaemonState, db: AsyncSession
) -> dict:
    """Compare current check results with previous results to detect changes."""
    rules = state["rules"]
    check_results = state["check_results"]
    drift_detections = []

    # Build lookup of current results
    current_by_rule = {r["rule_id"]: r for r in check_results}

    for rule in rules:
        rule_id = rule["id"]
        current = current_by_rule.get(rule_id, {})
        current_status = current.get("status", "unknown")
        previous_status = rule.get("last_result")

        # Detect drift: status changed from previous check
        if previous_status and current_status != previous_status:
            drift_type = "degradation" if current_status == "fail" else "improvement"
            if current_status == "error":
                drift_type = "error"

            drift_detections.append({
                "rule_id": rule_id,
                "rule_title": rule["title"],
                "previous_status": previous_status,
                "current_status": current_status,
                "drift_type": drift_type,
                "detected_at": datetime.now(timezone.utc).isoformat(),
            })

    return {"drift_detections": drift_detections}


async def generate_summary(
    state: MonitoringDaemonState, db: AsyncSession
) -> dict:
    """Compile summary of all checks, drift detections, and alerts."""
    rules = state["rules"]
    check_results = state["check_results"]
    drift_detections = state.get("drift_detections", [])

    # Aggregate results
    total_rules = len(rules)
    passed = sum(1 for r in check_results if r["status"] == "pass")
    failed = sum(1 for r in check_results if r["status"] == "fail")
    errored = sum(1 for r in check_results if r["status"] == "error")
    total_alerts = sum(r.get("alerts_count", 0) for r in check_results)

    # Collect all generated alert IDs
    all_alert_ids = []
    for r in check_results:
        all_alert_ids.extend(r.get("alert_ids", []))

    summary = {
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "total_rules_checked": total_rules,
        "passed": passed,
        "failed": failed,
        "errored": errored,
        "pass_rate": round((passed / total_rules * 100), 1) if total_rules > 0 else 0.0,
        "total_alerts_generated": total_alerts,
        "alert_ids": all_alert_ids,
        "drift_detections": drift_detections,
        "drift_count": len(drift_detections),
        "check_results": check_results,
    }

    return {"summary": summary, "alerts_generated": all_alert_ids}
