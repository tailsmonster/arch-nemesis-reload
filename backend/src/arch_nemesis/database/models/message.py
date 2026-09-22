from dataclasses import dataclass


@dataclass(frozen=True)
class MessageRecord:
    id: str
    game_id: str
    role: str
    content: str
    created_at: str
