from pydantic import BaseModel


class LLMCallResult(BaseModel):
    text: str
    provider: str
    model: str
    prompt_hash: str
    latency_ms: int
    success: bool = True
    error: str | None = None
