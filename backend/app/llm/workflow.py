from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.llm.dry_run import generate_nemesis_response, judge_argument
from app.models import GameState, JudgeResult


class TurnWorkflowState(TypedDict):
    game: GameState
    player_argument: str
    nemesis_response: str
    judgement: JudgeResult | None


def nemesis_node(state: TurnWorkflowState) -> TurnWorkflowState:
    return {
        **state,
        "nemesis_response": generate_nemesis_response(state["player_argument"], state["game"]),
    }


def judge_node(state: TurnWorkflowState) -> TurnWorkflowState:
    return {
        **state,
        "judgement": judge_argument(state["player_argument"], state["game"]),
    }


def build_turn_graph():
    graph = StateGraph(TurnWorkflowState)
    graph.add_node("nemesis", nemesis_node)
    graph.add_node("judge", judge_node)
    graph.set_entry_point("nemesis")
    graph.add_edge("nemesis", "judge")
    graph.add_edge("judge", END)
    return graph.compile()


turn_graph = build_turn_graph()


def run_turn_workflow(game: GameState, player_argument: str) -> tuple[str, JudgeResult]:
    result = turn_graph.invoke(
        {
            "game": game,
            "player_argument": player_argument,
            "nemesis_response": "",
            "judgement": None,
        }
    )
    judgement = result["judgement"]
    if judgement is None:
        raise RuntimeError("Judge node did not produce a judgement.")
    return result["nemesis_response"], judgement
