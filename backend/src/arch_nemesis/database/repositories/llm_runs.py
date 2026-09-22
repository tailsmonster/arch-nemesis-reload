from uuid import uuid4

from arch_nemesis.database.connection import get_connection
from arch_nemesis.database.repositories.games import utc_now


def record_llm_run(
    agent_name: str,
    provider: str,
    model: str,
    prompt_hash: str,
    latency_ms: int,
    success: bool,
    game_id: str | None = None,
    turn_id: str | None = None,
    error: str | None = None,
    response_preview: str | None = None,
) -> dict:
    run_id = str(uuid4())
    now = utc_now()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO llm_runs
            (id, game_id, turn_id, agent_name, provider, model, prompt_hash, latency_ms, success, error, response_preview, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                game_id,
                turn_id,
                agent_name,
                provider,
                model,
                prompt_hash,
                latency_ms,
                int(success),
                error,
                response_preview,
                now,
            ),
        )
    return {"id": run_id, "created_at": now}
