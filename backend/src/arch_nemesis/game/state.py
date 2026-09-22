from typing import Literal

from pydantic import BaseModel


class GameState(BaseModel):
    status: Literal["active", "won", "lost"] = "active"
    persuasion: int = 0
    anger: int = 0
    turn_count: int = 0
