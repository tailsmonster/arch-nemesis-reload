from arch_nemesis.agents.fact_checker.service import fact_check
from arch_nemesis.graph.state import TurnGraphState


def fact_check_node(state: TurnGraphState) -> TurnGraphState:
    result = fact_check(state["argument"], game_id=state["game_id"])
    return {
        **state,
        "fact_check": result,
        "nodes_visited": [*state.get("nodes_visited", []), "fact_check"],
    }
