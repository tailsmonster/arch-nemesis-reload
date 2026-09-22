from datetime import UTC, datetime
from uuid import uuid4

from arch_nemesis.database.connection import get_connection


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def create_game(title: str = "New Nemesis Session") -> dict:
    game_id = str(uuid4())
    now = utc_now()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO games (id, title, status, persuasion, anger, turn_count, created_at, updated_at)
            VALUES (?, ?, 'active', 0, 0, 0, ?, ?)
            """,
            (game_id, title, now, now),
        )
    return get_game(game_id)


def get_game(game_id: str) -> dict | None:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM games WHERE id = ?", (game_id,)).fetchone()
    return dict(row) if row else None


def list_games() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute("SELECT * FROM games ORDER BY updated_at DESC").fetchall()
    return [dict(row) for row in rows]


def update_game_state(game_id: str, persuasion_delta: int, anger_delta: int) -> dict:
    now = utc_now()
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE games
            SET persuasion = max(0, min(100, persuasion + ?)),
                anger = max(0, min(100, anger + ?)),
                turn_count = turn_count + 1,
                status = CASE
                    WHEN persuasion + ? >= 100 THEN 'won'
                    WHEN anger + ? >= 100 THEN 'lost'
                    ELSE status
                END,
                updated_at = ?
            WHERE id = ?
            """,
            (persuasion_delta, anger_delta, persuasion_delta, anger_delta, now, game_id),
        )
    return get_game(game_id)
