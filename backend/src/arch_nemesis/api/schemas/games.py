from pydantic import BaseModel, Field


class CreateGameRequest(BaseModel):
    title: str = Field(default="New Nemesis Session", min_length=1, max_length=120)


class MessageResponse(BaseModel):
    id: str
    game_id: str
    role: str
    content: str
    created_at: str


class GameResponse(BaseModel):
    id: str
    title: str
    status: str
    persuasion: int
    anger: int
    turn_count: int
    created_at: str
    updated_at: str


class GameDetailResponse(GameResponse):
    messages: list[MessageResponse]
