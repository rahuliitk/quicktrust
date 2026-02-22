"""LangGraph StateGraph wiring for controls generation."""
from langgraph.graph import StateGraph, END

from app.agents.controls_generation.state import ControlsGenerationState
from app.agents.controls_generation.nodes import (
    load_framework_requirements,
    match_templates_to_requirements,
    customize_controls,
    deduplicate_controls,
    suggest_owners,
    finalize_output,
)


def build_graph():
    """Build the LangGraph state graph for controls generation."""
    graph = StateGraph(ControlsGenerationState)

    # We register placeholder nodes — actual execution passes db via closure
    graph.add_node("load_framework_requirements", lambda state: state)
    graph.add_node("match_templates_to_requirements", lambda state: state)
    graph.add_node("customize_controls", lambda state: state)
    graph.add_node("deduplicate_controls", lambda state: state)
    graph.add_node("suggest_owners", lambda state: state)
    graph.add_node("finalize_output", lambda state: state)

    graph.set_entry_point("load_framework_requirements")
    graph.add_edge("load_framework_requirements", "match_templates_to_requirements")
    graph.add_edge("match_templates_to_requirements", "customize_controls")
    graph.add_edge("customize_controls", "deduplicate_controls")
    graph.add_edge("deduplicate_controls", "suggest_owners")
    graph.add_edge("suggest_owners", "finalize_output")
    graph.add_edge("finalize_output", END)

    return graph.compile()


async def run_controls_generation(
    db,
    org_id: str,
    agent_run_id: str,
    framework_id: str,
    company_context: dict,
) -> dict:
    """
    Run the full controls generation pipeline.
    We execute nodes sequentially with DB access rather than using LangGraph's
    built-in execution, since each node needs the async DB session.
    """
    state: ControlsGenerationState = {
        "org_id": org_id,
        "agent_run_id": agent_run_id,
        "framework_id": framework_id,
        "company_context": company_context,
    }

    # Execute nodes in sequence
    node_funcs = [
        ("load_framework_requirements", load_framework_requirements),
        ("match_templates_to_requirements", match_templates_to_requirements),
        ("customize_controls", customize_controls),
        ("deduplicate_controls", deduplicate_controls),
        ("suggest_owners", suggest_owners),
        ("finalize_output", finalize_output),
    ]

    for node_name, node_func in node_funcs:
        result = await node_func(state, db)
        if result:
            state.update(result)

        if state.get("error") and node_name == "load_framework_requirements":
            raise RuntimeError(state["error"])

    return {
        "controls_count": state.get("controls_count", 0),
        "controls": state.get("final_controls", []),
    }
