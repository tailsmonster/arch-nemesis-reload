from pydantic import BaseModel


class RuleApplication(BaseModel):
    persuasion_delta: int
    anger_delta: int
    reason: str
