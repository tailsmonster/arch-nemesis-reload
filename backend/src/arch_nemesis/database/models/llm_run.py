from dataclasses import dataclass


@dataclass(frozen=True)
class LLMRunRecord:
    id: str
    agent_name: str
    provider: str
    model: str
    prompt_hash: str
    latency_ms: int
    success: bool
    created_at: str
