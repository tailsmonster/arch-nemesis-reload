from uuid import uuid4

from arch_nemesis.database.connection import get_connection
from arch_nemesis.database.repositories.games import utc_now


def create_message(game_id: str, role: str, content: str) -> dict:
    message_id = str(uuid4())
    now = utc_now()
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO messages (id, game_id, role, content, created_at) VALUES (?, ?, ?, ?, ?)",
            (message_id, game_id, role, content, now),
        )
    return get_message(message_id)


def get_message(message_id: str) -> dict | None:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM messages WHERE id = ?", (message_id,)).fetchone()
    return dict(row) if row else None


def list_messages_for_game(game_id: str) -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM messages WHERE game_id = ? ORDER BY created_at ASC", (game_id,)
        ).fetchall()
    return [dict(row) for row in rows]
