from dataclasses import dataclass


@dataclass(frozen=True)
class GameRecord:
    id: str
    title: str
    status: str
    persuasion: int
    anger: int
    turn_count: int
    created_at: str
    updated_at: str
