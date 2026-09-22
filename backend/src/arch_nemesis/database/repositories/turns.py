from uuid import uuid4

from arch_nemesis.database.connection import get_connection
from arch_nemesis.database.repositories.games import utc_now


def create_turn(
    game_id: str, player_message_id: str, nemesis_message_id: str | None, turn_number: int
) -> dict:
    turn_id = str(uuid4())
    now = utc_now()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO turns (id, game_id, player_message_id, nemesis_message_id, turn_number, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (turn_id, game_id, player_message_id, nemesis_message_id, turn_number, now),
        )
    return get_turn(turn_id)


def get_turn(turn_id: str) -> dict | None:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM turns WHERE id = ?", (turn_id,)).fetchone()
    return dict(row) if row else None
