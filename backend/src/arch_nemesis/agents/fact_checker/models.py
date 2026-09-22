from pydantic import BaseModel, Field


class FactCheckResult(BaseModel):
    summary: str
    factuality_score: int = Field(ge=0, le=10)
    notable_claims: list[str] = Field(default_factory=list)
    concerns: list[str] = Field(default_factory=list)
