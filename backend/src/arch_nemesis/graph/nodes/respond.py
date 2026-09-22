from arch_nemesis.agents.nemesis.service import respond
from arch_nemesis.graph.state import TurnGraphState


def respond_node(state: TurnGraphState) -> TurnGraphState:
    result = respond(state["argument"], state["game"], state["rules"], game_id=state["game_id"])
    return {
        **state,
        "nemesis_response": result,
        "nodes_visited": [*state.get("nodes_visited", []), "respond"],
    }
