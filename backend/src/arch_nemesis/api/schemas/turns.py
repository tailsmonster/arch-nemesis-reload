from pydantic import BaseModel, Field

from arch_nemesis.api.schemas.games import GameDetailResponse


class SubmitTurnRequest(BaseModel):
    argument: str = Field(min_length=1, max_length=4000)


class SubmitTurnResponse(BaseModel):
    game: GameDetailResponse
    turn: dict
    evaluation: dict
    graph_run: dict | None = None
