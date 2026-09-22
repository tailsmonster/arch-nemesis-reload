from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, Field


class GameStatus(StrEnum):
    ACTIVE = "active"
    WON = "won"
    LOST = "lost"


class PlayMode(StrEnum):
    CHAT = "chat"
    FIGHT = "fight"
    COMPLETE = "complete"


class RoundStatus(StrEnum):
    ACTIVE = "active"
    COMPLETE = "complete"


class ArgumentQuality(StrEnum):
    WEAK = "weak"
    OK = "ok"
    STRONG = "strong"


class GameState(BaseModel):
    id: str
    active_round_id: str
    persuasion: int
    anger: int
    strikes: int
    turn_count: int
    status: GameStatus
    mode: PlayMode
    created_at: datetime
    updated_at: datetime


class Round(BaseModel):
    id: str
    game_id: str
    round_number: int
    status: RoundStatus
    created_at: datetime
    updated_at: datetime


class JudgeResult(BaseModel):
    persuasion_delta: int = Field(ge=-5, le=10)
    anger_delta: int = Field(ge=-5, le=10)
    reasoning: str = Field(min_length=1, max_length=1000)
    argument_quality: ArgumentQuality


class Turn(BaseModel):
    id: str
    game_id: str
    round_id: str
    turn_number: int
    player_argument: str
    nemesis_response: str
    persuasion_delta: int
    anger_delta: int
    judge_reasoning: str
    argument_quality: ArgumentQuality
    strike_delta: int
    created_at: datetime


class GameEvent(BaseModel):
    id: str
    game_id: str
    round_id: str | None
    turn_id: str | None
    event_type: str
    message: str
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
    active_round: Round
    turns: list[Turn]
    events: list[GameEvent]


class GameListResponse(BaseModel):
    games: list[GameState]


class HealthResponse(BaseModel):
    status: str


class DebugNemesisResponse(BaseModel):
    nemesis_response: str


class DebugJudgeResponse(BaseModel):
    judgement: JudgeResult


class TurnPreviewResponse(BaseModel):
    game: GameState
    preview_game: GameState
    nemesis_response: str
    judgement: JudgeResult
