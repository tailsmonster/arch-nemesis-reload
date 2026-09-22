from dataclasses import dataclass


@dataclass(frozen=True)
class TurnRecord:
    id: str
    game_id: str
    player_message_id: str
    nemesis_message_id: str | None
    turn_number: int
    created_at: str
