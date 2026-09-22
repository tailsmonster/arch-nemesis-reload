from arch_nemesis.agents.director.service import evaluate_turn
from arch_nemesis.graph.state import TurnGraphState


def director_evaluate_node(state: TurnGraphState) -> TurnGraphState:
    result = evaluate_turn(
        state["argument"], state["game"], state["fact_check"], game_id=state["game_id"]
    )
    return {
        **state,
        "director_evaluation": result,
        "nodes_visited": [*state.get("nodes_visited", []), "director_evaluate"],
    }
