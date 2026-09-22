from langgraph.graph import END, StateGraph

from arch_nemesis.graph.edges.routing import APPLICATION_FLOW_NODES, LINEAR_TURN_FLOW
from arch_nemesis.graph.nodes.apply_rules import apply_rules_node
from arch_nemesis.graph.nodes.director_evaluate import director_evaluate_node
from arch_nemesis.graph.nodes.fact_check import fact_check_node
from arch_nemesis.graph.nodes.load_context import load_context_node
from arch_nemesis.graph.nodes.persist import persist_node
from arch_nemesis.graph.nodes.respond import respond_node
from arch_nemesis.graph.state import TurnGraphState


NODES = {
    "load_context": load_context_node,
    "llm_fact_check": fact_check_node,
    "llm_director_evaluate": director_evaluate_node,
    "apply_rules": apply_rules_node,
    "llm_nemesis_respond": respond_node,
    "persist_turn": persist_node,
}

APPLICATION_NODE_METADATA = {
    "client_chat_ui": {
        "label": "Client Chat UI",
        "kind": "client",
        "description": "Future React game surface that displays state and sends turns.",
    },
    "api_create_or_select_game": {
        "label": "Create / Select Game",
        "kind": "api",
        "description": "POST /api/games, GET /api/games, or GET /api/games/{game_id}.",
    },
    "api_select_round_id": {
        "label": "Select Round / Turn ID",
        "kind": "api",
        "description": "Load a specific round/turn context for replay, inspection, or continuation.",
    },
    "db_load_game_context": {
        "label": "DB Load Context",
        "kind": "database",
        "description": "Load game, prior messages, turns, evaluations, graph runs, and LLM traces.",
    },
    "api_submit_player_argument": {
        "label": "Submit Player Argument",
        "kind": "api",
        "description": "POST /api/games/{game_id}/turns.",
    },
    "graph_turn_start": {
        "label": "LangGraph Turn Start",
        "kind": "graph",
        "description": "Enter the executable LangGraph turn workflow.",
    },
    "load_context": {
        "label": "Load Context",
        "kind": "graph_node",
        "description": "Create the player message and load canonical game state.",
    },
    "llm_fact_check": {
        "label": "llm_fact_check",
        "kind": "llm_node",
        "description": "Fact checker LLM evaluates factual claims in the player's argument.",
    },
    "llm_director_evaluate": {
        "label": "llm_director_evaluate",
        "kind": "llm_node",
        "description": "Director LLM evaluates persuasion strategy and game consequences.",
    },
    "apply_rules": {
        "label": "Apply Rules",
        "kind": "deterministic_node",
        "description": "Python clamps and applies authoritative scoring rules.",
    },
    "llm_nemesis_respond": {
        "label": "llm_nemesis_respond",
        "kind": "llm_node",
        "description": "Nemesis LLM produces the in-character hostile Arch zealot reply.",
    },
    "persist_turn": {
        "label": "Persist Turn",
        "kind": "database_node",
        "description": "Persist messages, turn, evaluation, LLM runs, graph run, and updated game state.",
    },
    "api_return_updated_state": {
        "label": "Return Updated State",
        "kind": "api",
        "description": "Return updated game, messages, turn, evaluation, and graph metadata.",
    },
    "client_render_state": {
        "label": "Client Renders State",
        "kind": "client",
        "description": "Frontend later renders messages, meters, status, and trace links.",
    },
    "await_next_player_turn": {
        "label": "Await Next Player Turn",
        "kind": "loop",
        "description": "The next submitted argument loops back through selected game/round context.",
    },
}

APPLICATION_EDGES = [
    {"from": "client_chat_ui", "to": "api_create_or_select_game", "label": "start/load"},
    {"from": "api_create_or_select_game", "to": "api_select_round_id", "label": "selected game"},
    {"from": "api_select_round_id", "to": "db_load_game_context", "label": "game_id + optional turn_id"},
    {"from": "db_load_game_context", "to": "api_submit_player_argument", "label": "context"},
    {"from": "api_submit_player_argument", "to": "graph_turn_start", "label": "invoke graph"},
    {"from": "graph_turn_start", "to": "load_context", "label": "TurnGraphState"},
    *[
        {"from": left, "to": right, "label": "next"}
        for left, right in zip(LINEAR_TURN_FLOW, LINEAR_TURN_FLOW[1:])
    ],
    {"from": "persist_turn", "to": "api_return_updated_state", "label": "saved canonical state"},
    {"from": "api_return_updated_state", "to": "client_render_state", "label": "JSON response"},
    {"from": "client_render_state", "to": "await_next_player_turn", "label": "display"},
    {"from": "await_next_player_turn", "to": "api_select_round_id", "label": "next turn / inspect round"},
]


def build_turn_graph():
    graph = StateGraph(TurnGraphState)
    for name, node in NODES.items():
        graph.add_node(name, node)
    graph.set_entry_point("load_context")
    for left, right in zip(LINEAR_TURN_FLOW, LINEAR_TURN_FLOW[1:]):
        graph.add_edge(left, right)
    graph.add_edge("persist_turn", END)
    return graph.compile()


def get_graph_spec() -> dict:
    return {
        "title": "Arch Nemesis Application Graph",
        "version": "0.1.0",
        "executable_langgraph": {
            "builder": "backend/src/arch_nemesis/graph/builder.py",
            "function": "build_turn_graph",
            "add_node_lines": "graph.add_node(name, node) in build_turn_graph",
            "entry_point": "load_context",
            "nodes": LINEAR_TURN_FLOW,
        },
        "nodes": [
            {"id": node_id, **APPLICATION_NODE_METADATA[node_id]}
            for node_id in APPLICATION_FLOW_NODES
        ],
        "edges": APPLICATION_EDGES,
    }


def get_graph_mermaid() -> str:
    spec = get_graph_spec()
    lines = ["flowchart TD"]
    lines.extend(
        [
            "    subgraph Client[Client / Future Frontend]",
            "        client_chat_ui[\"Client Chat UI\"]",
            "        client_render_state[\"Client Renders State\"]",
            "        await_next_player_turn[\"Await Next Player Turn\"]",
            "    end",
            "    subgraph API[FastAPI Game API]",
            "        api_create_or_select_game[\"Create / Select Game\"]",
            "        api_select_round_id[\"Select Round / Turn ID\"]",
            "        api_submit_player_argument[\"Submit Player Argument\"]",
            "        api_return_updated_state[\"Return Updated State\"]",
            "    end",
            "    subgraph DB[SQLite Canonical State]",
            "        db_load_game_context[\"DB Load Context\"]",
            "    end",
            "    subgraph LG[LangGraph Executable Turn Workflow]",
            "        graph_turn_start[\"LangGraph Turn Start\"]",
            "        load_context[\"Load Context\"]",
            "        llm_fact_check[\"llm_fact_check\"]",
            "        llm_director_evaluate[\"llm_director_evaluate\"]",
            "        apply_rules[\"Apply Rules\"]",
            "        llm_nemesis_respond[\"llm_nemesis_respond\"]",
            "        persist_turn[\"Persist Turn\"]",
            "    end",
        ]
    )
    for edge in spec["edges"]:
        label = edge.get("label")
        if label:
            lines.append(f"    {edge['from']} -->|{label}| {edge['to']}")
        else:
            lines.append(f"    {edge['from']} --> {edge['to']}")
    lines.extend(
        [
            "    classDef llm fill:#ffe8cc,stroke:#f08c00,stroke-width:2px;",
            "    classDef db fill:#d3f9d8,stroke:#2f9e44,stroke-width:2px;",
            "    classDef api fill:#d0ebff,stroke:#1c7ed6,stroke-width:2px;",
            "    class llm_fact_check,llm_director_evaluate,llm_nemesis_respond llm;",
            "    class db_load_game_context,persist_turn db;",
            "    class api_create_or_select_game,api_select_round_id,api_submit_player_argument,api_return_updated_state api;",
        ]
    )
    return "\n".join(lines)
