import json
from uuid import uuid4

from arch_nemesis.database.connection import get_connection
from arch_nemesis.database.repositories.games import utc_now


def record_graph_run(
    status: str,
    nodes_visited: list[str],
    game_id: str | None = None,
    turn_id: str | None = None,
    error: str | None = None,
    completed_at: str | None = None,
) -> dict:
    run_id = str(uuid4())
    now = utc_now()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO graph_runs (id, game_id, turn_id, status, nodes_visited, error, created_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (run_id, game_id, turn_id, status, json.dumps(nodes_visited), error, now, completed_at),
        )
    return {"id": run_id, "created_at": now}
