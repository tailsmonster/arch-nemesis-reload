from arch_nemesis.database.repositories import messages
from arch_nemesis.graph.builder import build_turn_graph
from arch_nemesis.services.game_service import get_game_detail


def submit_turn(game_id: str, argument: str) -> dict:
    graph = build_turn_graph()
    state = graph.invoke({"game_id": game_id, "argument": argument, "nodes_visited": []})
    game = get_game_detail(game_id)
    return {
        "game": game,
        "turn": state["turn"],
        "evaluation": state["evaluation"],
        "graph_run": state.get("graph_run"),
    }
