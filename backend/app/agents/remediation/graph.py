"""LangGraph StateGraph wiring for remediation."""
from langgraph.graph import StateGraph, END

from app.agents.remediation.state import RemediationState
from app.agents.remediation.nodes import (
    load_failing_controls,
    generate_remediation_plans,
    prioritize,
    save_to_db,
)


def build_graph():
    """Build the LangGraph state graph for remediation."""
    graph = StateGraph(RemediationState)

    graph.add_node("load_failing_controls", lambda state: state)
    graph.add_node("generate_remediation_plans", lambda state: state)
    graph.add_node("prioritize", lambda state: state)
    graph.add_node("save_to_db", lambda state: state)

    graph.set_entry_point("load_failing_controls")
    graph.add_edge("load_failing_controls", "generate_remediation_plans")
    graph.add_edge("generate_remediation_plans", "prioritize")
    graph.add_edge("prioritize", "save_to_db")
    graph.add_edge("save_to_db", END)

    return graph.compile()


async def run_remediation(
    db,
    org_id: str,
    agent_run_id: str,
) -> dict:
    """
    Run the full remediation pipeline.
    Executes nodes sequentially with DB access rather than using LangGraph's
    built-in execution, since each node needs the async DB session.
    """
    state: RemediationState = {
        "org_id": org_id,
        "agent_run_id": agent_run_id,
    }

    node_funcs = [
        ("load_failing_controls", load_failing_controls),
        ("generate_remediation_plans", generate_remediation_plans),
        ("prioritize", prioritize),
        ("save_to_db", save_to_db),
    ]

    for node_name, node_func in node_funcs:
        result = await node_func(state, db)
        if result:
            state.update(result)

        if state.get("error") and node_name == "load_failing_controls":
            raise RuntimeError(state["error"])

    return {
        "saved_count": state.get("saved_count", 0),
        "plans": state.get("prioritized_plans", []),
    }
