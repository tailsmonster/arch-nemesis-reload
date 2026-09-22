import json
from uuid import uuid4

from arch_nemesis.database.connection import get_connection
from arch_nemesis.database.repositories.games import utc_now


def create_evaluation(
    turn_id: str,
    fact_check: str,
    argument_quality: int,
    persuasion_delta: int,
    anger_delta: int,
    reason: str,
    raw_output: dict,
) -> dict:
    evaluation_id = str(uuid4())
    now = utc_now()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO evaluations
            (id, turn_id, fact_check, argument_quality, persuasion_delta, anger_delta, reason, raw_output, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                evaluation_id,
                turn_id,
                fact_check,
                argument_quality,
                persuasion_delta,
                anger_delta,
                reason,
                json.dumps(raw_output),
                now,
            ),
        )
    return {"id": evaluation_id, "turn_id": turn_id, "created_at": now}
