"""Policy generation agent — orchestrates the pipeline."""
from langgraph.graph import StateGraph, END

from app.agents.policy_generation.state import PolicyGenerationState
from app.agents.policy_generation.nodes import (
    identify_required_policies,
    match_policy_templates,
    generate_policy_content,
    finalize_policies,
)


def build_graph():
    """Build the LangGraph state graph for policy generation."""
    graph = StateGraph(PolicyGenerationState)

    graph.add_node("identify_required_policies", lambda state: state)
    graph.add_node("match_policy_templates", lambda state: state)
    graph.add_node("generate_policy_content", lambda state: state)
    graph.add_node("finalize_policies", lambda state: state)

    graph.set_entry_point("identify_required_policies")
    graph.add_edge("identify_required_policies", "match_policy_templates")
    graph.add_edge("match_policy_templates", "generate_policy_content")
    graph.add_edge("generate_policy_content", "finalize_policies")
    graph.add_edge("finalize_policies", END)

    return graph.compile()


async def run_policy_generation(
    db,
    org_id: str,
    agent_run_id: str,
    framework_id: str,
    company_context: dict,
) -> dict:
    """
    Run the full policy generation pipeline.
    Sequential execution with DB access, matching the controls agent pattern.
    """
    state: PolicyGenerationState = {
        "org_id": org_id,
        "agent_run_id": agent_run_id,
        "framework_id": framework_id,
        "company_context": company_context,
    }

    node_funcs = [
        ("identify_required_policies", identify_required_policies),
        ("match_policy_templates", match_policy_templates),
        ("generate_policy_content", generate_policy_content),
        ("finalize_policies", finalize_policies),
    ]

    for node_name, node_func in node_funcs:
        result = await node_func(state, db)
        if result:
            state.update(result)

        if state.get("error"):
            raise RuntimeError(state["error"])

    return {
        "policies_count": state.get("policies_count", 0),
        "policies": state.get("final_policies", []),
    }
