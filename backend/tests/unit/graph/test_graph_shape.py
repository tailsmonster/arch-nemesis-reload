from arch_nemesis.graph.builder import get_graph_mermaid, get_graph_spec


def test_graph_spec_has_expected_nodes():
    spec = get_graph_spec()
    node_ids = [node["id"] for node in spec["nodes"]]
    assert node_ids == [
        "load_context",
        "fact_check",
        "director_evaluate",
        "apply_rules",
        "respond",
        "persist",
    ]


def test_mermaid_contains_turn_flow():
    mermaid = get_graph_mermaid()
    assert "load_context --> fact_check" in mermaid
    assert "respond --> persist" in mermaid
