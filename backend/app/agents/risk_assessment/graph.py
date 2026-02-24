"""LangGraph StateGraph wiring for risk assessment."""
from langgraph.graph import StateGraph, END

from app.agents.risk_assessment.state import RiskAssessmentState
from app.agents.risk_assessment.nodes import (
    load_controls,
    identify_risk_areas,
    score_risks,
    save_to_db,
)


def build_graph():
    """Build the LangGraph state graph for risk assessment."""
    graph = StateGraph(RiskAssessmentState)

    graph.add_node("load_controls", lambda state: state)
    graph.add_node("identify_risk_areas", lambda state: state)
    graph.add_node("score_risks", lambda state: state)
    graph.add_node("save_to_db", lambda state: state)

    graph.set_entry_point("load_controls")
    graph.add_edge("load_controls", "identify_risk_areas")
    graph.add_edge("identify_risk_areas", "score_risks")
    graph.add_edge("score_risks", "save_to_db")
    graph.add_edge("save_to_db", END)

    return graph.compile()


async def run_risk_assessment(
    db,
    org_id: str,
    agent_run_id: str,
    framework_id: str = None,
) -> dict:
    """
    Run the full risk assessment pipeline.
    Executes nodes sequentially with DB access rather than using LangGraph's
    built-in execution, since each node needs the async DB session.
    """
    state: RiskAssessmentState = {
        "org_id": org_id,
        "agent_run_id": agent_run_id,
        "framework_id": framework_id,
    }

    node_funcs = [
        ("load_controls", load_controls),
        ("identify_risk_areas", identify_risk_areas),
        ("score_risks", score_risks),
        ("save_to_db", save_to_db),
    ]

    for node_name, node_func in node_funcs:
        result = await node_func(state, db)
        if result:
            state.update(result)

        if state.get("error") and node_name == "load_controls":
            raise RuntimeError(state["error"])

    return {
        "risks_count": state.get("risks_count", 0),
        "risks": state.get("final_risks", []),
    }
