from pydantic import BaseModel, Field


class DirectorEvaluation(BaseModel):
    intent: str
    argument_quality: int = Field(ge=0, le=10)
    persuasion_delta: int = Field(ge=-10, le=10)
    anger_delta: int = Field(ge=-10, le=10)
    reason: str
