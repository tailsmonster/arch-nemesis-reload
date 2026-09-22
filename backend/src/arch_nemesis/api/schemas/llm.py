from pydantic import BaseModel, Field


class LLMTextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
    game_id: str | None = None


class LLMResponse(BaseModel):
    result: dict
