"""LangGraph StateGraph wiring for vendor risk assessment."""
from langgraph.graph import StateGraph, END

from app.agents.vendor_risk_assessment.state import VendorRiskAssessmentState
from app.agents.vendor_risk_assessment.nodes import (
    load_vendor_info,
    analyze_vendor_risk,
    score_vendor,
    save_assessment,
)


def build_graph():
    """Build the LangGraph state graph for vendor risk assessment."""
    graph = StateGraph(VendorRiskAssessmentState)

    graph.add_node("load_vendor_info", lambda state: state)
    graph.add_node("analyze_vendor_risk", lambda state: state)
    graph.add_node("score_vendor", lambda state: state)
    graph.add_node("save_assessment", lambda state: state)

    graph.set_entry_point("load_vendor_info")
    graph.add_edge("load_vendor_info", "analyze_vendor_risk")
    graph.add_edge("analyze_vendor_risk", "score_vendor")
    graph.add_edge("score_vendor", "save_assessment")
    graph.add_edge("save_assessment", END)

    return graph.compile()


async def run_vendor_risk_assessment(
    db,
    org_id: str,
    agent_run_id: str,
    vendor_id: str,
) -> dict:
    """
    Run the full vendor risk assessment pipeline.
    Executes nodes sequentially with DB access rather than using LangGraph's
    built-in execution, since each node needs the async DB session.
    """
    state: VendorRiskAssessmentState = {
        "org_id": org_id,
        "agent_run_id": agent_run_id,
        "vendor_id": vendor_id,
    }

    node_funcs = [
        ("load_vendor_info", load_vendor_info),
        ("analyze_vendor_risk", analyze_vendor_risk),
        ("score_vendor", score_vendor),
        ("save_assessment", save_assessment),
    ]

    for node_name, node_func in node_funcs:
        result = await node_func(state, db)
        if result:
            state.update(result)

        if state.get("error") and node_name == "load_vendor_info":
            raise RuntimeError(state["error"])

    return {
        "vendor_id": vendor_id,
        "risk_score": state.get("risk_score", 0),
        "recommendations": state.get("recommendations", []),
        "saved": state.get("saved", False),
    }
