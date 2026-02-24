"""LangGraph StateGraph wiring for audit preparation."""
from langgraph.graph import StateGraph, END

from app.agents.audit_preparation.state import AuditPreparationState
from app.agents.audit_preparation.nodes import (
    load_audit_scope,
    analyze_evidence_coverage,
    identify_gaps,
    generate_workpapers,
    save_findings,
)


def build_graph():
    """Build the LangGraph state graph for audit preparation."""
    graph = StateGraph(AuditPreparationState)

    graph.add_node("load_audit_scope", lambda state: state)
    graph.add_node("analyze_evidence_coverage", lambda state: state)
    graph.add_node("identify_gaps", lambda state: state)
    graph.add_node("generate_workpapers", lambda state: state)
    graph.add_node("save_findings", lambda state: state)

    graph.set_entry_point("load_audit_scope")
    graph.add_edge("load_audit_scope", "analyze_evidence_coverage")
    graph.add_edge("analyze_evidence_coverage", "identify_gaps")
    graph.add_edge("identify_gaps", "generate_workpapers")
    graph.add_edge("generate_workpapers", "save_findings")
    graph.add_edge("save_findings", END)

    return graph.compile()


async def run_audit_preparation(
    db,
    org_id: str,
    agent_run_id: str,
    audit_id: str,
) -> dict:
    """
    Run the full audit preparation pipeline.
    Executes nodes sequentially with DB access rather than using LangGraph's
    built-in execution, since each node needs the async DB session.
    """
    state: AuditPreparationState = {
        "org_id": org_id,
        "agent_run_id": agent_run_id,
        "audit_id": audit_id,
    }

    node_funcs = [
        ("load_audit_scope", load_audit_scope),
        ("analyze_evidence_coverage", analyze_evidence_coverage),
        ("identify_gaps", identify_gaps),
        ("generate_workpapers", generate_workpapers),
        ("save_findings", save_findings),
    ]

    for node_name, node_func in node_funcs:
        result = await node_func(state, db)
        if result:
            state.update(result)

        if state.get("error") and node_name == "load_audit_scope":
            raise RuntimeError(state["error"])

    return {
        "readiness_assessment": state.get("readiness_assessment", {}),
        "gaps": state.get("gaps", []),
        "workpapers": state.get("workpapers", []),
    }
