"""Evidence generation agent — orchestrates the pipeline."""
from langgraph.graph import StateGraph, END

from app.agents.evidence_generation.state import EvidenceGenerationState
from app.agents.evidence_generation.nodes import (
    load_controls,
    match_evidence_templates,
    generate_evidence_data,
    finalize_evidence,
)


def build_graph():
    """Build the LangGraph state graph for evidence generation."""
    graph = StateGraph(EvidenceGenerationState)

    graph.add_node("load_controls", lambda state: state)
    graph.add_node("match_evidence_templates", lambda state: state)
    graph.add_node("generate_evidence_data", lambda state: state)
    graph.add_node("finalize_evidence", lambda state: state)

    graph.set_entry_point("load_controls")
    graph.add_edge("load_controls", "match_evidence_templates")
    graph.add_edge("match_evidence_templates", "generate_evidence_data")
    graph.add_edge("generate_evidence_data", "finalize_evidence")
    graph.add_edge("finalize_evidence", END)

    return graph.compile()


async def run_evidence_generation(
    db,
    org_id: str,
    agent_run_id: str,
    company_context: dict,
) -> dict:
    """
    Run the full evidence generation pipeline.
    Sequential execution with DB access, matching the controls/policy agent pattern.
    """
    state: EvidenceGenerationState = {
        "org_id": org_id,
        "agent_run_id": agent_run_id,
        "company_context": company_context,
    }

    node_funcs = [
        ("load_controls", load_controls),
        ("match_evidence_templates", match_evidence_templates),
        ("generate_evidence_data", generate_evidence_data),
        ("finalize_evidence", finalize_evidence),
    ]

    for node_name, node_func in node_funcs:
        result = await node_func(state, db)
        if result:
            state.update(result)

        if state.get("error"):
            raise RuntimeError(state["error"])

    return {
        "evidence_count": state.get("evidence_count", 0),
        "evidence": state.get("final_evidence", []),
    }
