from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, Field


class GameStatus(StrEnum):
    ACTIVE = "active"
    WON = "won"
    LOST = "lost"


class ArgumentQuality(StrEnum):
    WEAK = "weak"
    OK = "ok"
    STRONG = "strong"


class GameState(BaseModel):
    id: int
    persuasion: int
    anger: int
    turn_count: int
    status: GameStatus
    created_at: datetime
    updated_at: datetime


class JudgeResult(BaseModel):
    persuasion_delta: int = Field(ge=-5, le=10)
    anger_delta: int = Field(ge=-5, le=10)
    reasoning: str = Field(min_length=1, max_length=1000)
    argument_quality: ArgumentQuality


class Turn(BaseModel):
    id: int
    game_id: int
    turn_number: int
    player_argument: str
    nemesis_response: str
    persuasion_delta: int
    anger_delta: int
    judge_reasoning: str
    argument_quality: ArgumentQuality
    created_at: datetime


class CreateGameResponse(BaseModel):
    game: GameState
    turns: list[Turn]


class SubmitArgumentRequest(BaseModel):
    argument: str = Field(min_length=1, max_length=4000)


class SubmitArgumentResponse(BaseModel):
    game: GameState
    turn: Turn
    turns: list[Turn]


class GameDetailResponse(BaseModel):
    game: GameState
    turns: list[Turn]
