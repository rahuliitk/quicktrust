"""LangGraph StateGraph wiring for monitoring daemon."""
from langgraph.graph import StateGraph, END

from app.agents.monitoring_daemon.state import MonitoringDaemonState
from app.agents.monitoring_daemon.nodes import (
    load_active_rules,
    run_all_checks,
    detect_drift,
    generate_summary,
)


def build_graph():
    """Build the LangGraph state graph for monitoring daemon."""
    graph = StateGraph(MonitoringDaemonState)

    graph.add_node("load_active_rules", lambda state: state)
    graph.add_node("run_all_checks", lambda state: state)
    graph.add_node("detect_drift", lambda state: state)
    graph.add_node("generate_summary", lambda state: state)

    graph.set_entry_point("load_active_rules")
    graph.add_edge("load_active_rules", "run_all_checks")
    graph.add_edge("run_all_checks", "detect_drift")
    graph.add_edge("detect_drift", "generate_summary")
    graph.add_edge("generate_summary", END)

    return graph.compile()


async def run_monitoring_daemon(
    db,
    org_id: str,
    agent_run_id: str,
) -> dict:
    """
    Run the full monitoring daemon pipeline.
    Executes nodes sequentially with DB access rather than using LangGraph's
    built-in execution, since each node needs the async DB session.
    """
    state: MonitoringDaemonState = {
        "org_id": org_id,
        "agent_run_id": agent_run_id,
    }

    node_funcs = [
        ("load_active_rules", load_active_rules),
        ("run_all_checks", run_all_checks),
        ("detect_drift", detect_drift),
        ("generate_summary", generate_summary),
    ]

    for node_name, node_func in node_funcs:
        result = await node_func(state, db)
        if result:
            state.update(result)

        if state.get("error") and node_name == "load_active_rules":
            raise RuntimeError(state["error"])

    return {
        "summary": state.get("summary", {}),
    }
