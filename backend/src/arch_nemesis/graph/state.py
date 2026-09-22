from typing import TypedDict


class TurnGraphState(TypedDict, total=False):
    game_id: str
    argument: str
    game: dict
    player_message: dict
    fact_check: object
    director_evaluation: object
    rules: object
    nemesis_response: object
    nemesis_message: dict
    turn: dict
    evaluation: dict
    nodes_visited: list[str]
