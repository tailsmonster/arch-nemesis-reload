from arch_nemesis.database.repositories import games, messages
from arch_nemesis.graph.state import TurnGraphState


def load_context_node(state: TurnGraphState) -> TurnGraphState:
    game = games.get_game(state["game_id"])
    if not game:
        raise ValueError("Game not found")
    player_message = messages.create_message(state["game_id"], "player", state["argument"])
    return {
        **state,
        "game": game,
        "player_message": player_message,
        "nodes_visited": [*state.get("nodes_visited", []), "load_context"],
    }
