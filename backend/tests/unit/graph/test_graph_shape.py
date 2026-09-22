from arch_nemesis.graph.builder import get_graph_mermaid, get_graph_spec


def test_graph_spec_has_expected_nodes():
    spec = get_graph_spec()
    node_ids = [node["id"] for node in spec["nodes"]]
    assert "api_select_round_id" in node_ids
    assert "db_load_game_context" in node_ids
    assert "llm_fact_check" in node_ids
    assert "llm_director_evaluate" in node_ids
    assert "llm_nemesis_respond" in node_ids
    assert "await_next_player_turn" in node_ids


def test_graph_spec_declares_executable_langgraph_add_nodes():
    spec = get_graph_spec()
    executable = spec["executable_langgraph"]
    assert executable["function"] == "build_turn_graph"
    assert "graph.add_node" in executable["add_node_lines"]
    assert executable["nodes"] == [
        "load_context",
        "llm_fact_check",
        "llm_director_evaluate",
        "apply_rules",
        "llm_nemesis_respond",
        "persist_turn",
    ]


def test_mermaid_contains_turn_flow():
    mermaid = get_graph_mermaid()
    assert "load_context -->|next| llm_fact_check" in mermaid
    assert "llm_nemesis_respond -->|next| persist_turn" in mermaid
    assert "await_next_player_turn -->|next turn / inspect round| api_select_round_id" in mermaid
