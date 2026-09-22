from langgraph.graph import END, StateGraph

from arch_nemesis.graph.edges.routing import LINEAR_TURN_FLOW
from arch_nemesis.graph.nodes.apply_rules import apply_rules_node
from arch_nemesis.graph.nodes.director_evaluate import director_evaluate_node
from arch_nemesis.graph.nodes.fact_check import fact_check_node
from arch_nemesis.graph.nodes.load_context import load_context_node
from arch_nemesis.graph.nodes.persist import persist_node
from arch_nemesis.graph.nodes.respond import respond_node
from arch_nemesis.graph.state import TurnGraphState


NODES = {
    "load_context": load_context_node,
    "fact_check": fact_check_node,
    "director_evaluate": director_evaluate_node,
    "apply_rules": apply_rules_node,
    "respond": respond_node,
    "persist": persist_node,
}


def build_turn_graph():
    graph = StateGraph(TurnGraphState)
    for name, node in NODES.items():
        graph.add_node(name, node)
    graph.set_entry_point("load_context")
    for left, right in zip(LINEAR_TURN_FLOW, LINEAR_TURN_FLOW[1:]):
        graph.add_edge(left, right)
    graph.add_edge("persist", END)
    return graph.compile()


def get_graph_spec() -> dict:
    edges = [
        {"from": left, "to": right}
        for left, right in zip(LINEAR_TURN_FLOW, LINEAR_TURN_FLOW[1:])
    ] + [{"from": "persist", "to": "END"}]
    return {
        "title": "Arch Nemesis Turn Graph",
        "version": "0.1.0",
        "nodes": [{"id": node, "label": node.replace("_", " ").title()} for node in LINEAR_TURN_FLOW],
        "edges": edges,
    }


def get_graph_mermaid() -> str:
    lines = ["flowchart TD"]
    for node in LINEAR_TURN_FLOW:
        lines.append(f'    {node}["{node.replace("_", " ").title()}"]')
    for left, right in zip(LINEAR_TURN_FLOW, LINEAR_TURN_FLOW[1:]):
        lines.append(f"    {left} --> {right}")
    lines.append("    persist --> END")
    return "\n".join(lines)
