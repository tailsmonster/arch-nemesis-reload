from arch_nemesis.database.repositories.llm_runs import record_llm_run
from arch_nemesis.llm.models import LLMCallResult


def trace_llm_result(agent_name: str, result: LLMCallResult, game_id: str | None = None) -> dict:
    return record_llm_run(
        agent_name=agent_name,
        provider=result.provider,
        model=result.model,
        prompt_hash=result.prompt_hash,
        latency_ms=result.latency_ms,
        success=result.success,
        game_id=game_id,
        error=result.error,
        response_preview=result.text[:300],
    )
