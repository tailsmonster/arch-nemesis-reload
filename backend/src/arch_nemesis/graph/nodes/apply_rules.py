from arch_nemesis.game.engine import evaluate_game_impact
from arch_nemesis.graph.state import TurnGraphState


def apply_rules_node(state: TurnGraphState) -> TurnGraphState:
    rules = evaluate_game_impact(state["director_evaluation"])
    return {
        **state,
        "rules": rules,
        "nodes_visited": [*state.get("nodes_visited", []), "apply_rules"],
    }
