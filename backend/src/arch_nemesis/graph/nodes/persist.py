from arch_nemesis.database.repositories import evaluations, games, graph_runs, messages, turns
from arch_nemesis.database.repositories.games import utc_now
from arch_nemesis.graph.state import TurnGraphState


def persist_node(state: TurnGraphState) -> TurnGraphState:
    nemesis_message = messages.create_message(
        state["game_id"], "nemesis", state["nemesis_response"].content
    )
    updated_game = games.update_game_state(
        state["game_id"], state["rules"].persuasion_delta, state["rules"].anger_delta
    )
    turn = turns.create_turn(
        state["game_id"],
        state["player_message"]["id"],
        nemesis_message["id"],
        updated_game["turn_count"],
    )
    evaluation = evaluations.create_evaluation(
        turn_id=turn["id"],
        fact_check=state["fact_check"].summary,
        argument_quality=state["director_evaluation"].argument_quality,
        persuasion_delta=state["rules"].persuasion_delta,
        anger_delta=state["rules"].anger_delta,
        reason=state["rules"].reason,
        raw_output={
            "fact_check": state["fact_check"].model_dump(),
            "director": state["director_evaluation"].model_dump(),
        },
    )
    visited = [*state.get("nodes_visited", []), "persist"]
    graph_run = graph_runs.record_graph_run(
        "success", visited, game_id=state["game_id"], turn_id=turn["id"], completed_at=utc_now()
    )
    return {
        **state,
        "game": updated_game,
        "nemesis_message": nemesis_message,
        "turn": turn,
        "evaluation": evaluation,
        "graph_run": graph_run,
        "nodes_visited": visited,
    }
