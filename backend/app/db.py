import sqlite3
from collections.abc import Iterable
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from app.models import ArgumentQuality, GameState, GameStatus, JudgeResult, Turn


def encode_dt(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def decode_dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


class Database:
    def __init__(self, path: str):
        self.path = path

    @contextmanager
    def connect(self):
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    persuasion INTEGER NOT NULL,
                    anger INTEGER NOT NULL,
                    turn_count INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS turns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id INTEGER NOT NULL REFERENCES games(id),
                    turn_number INTEGER NOT NULL,
                    player_argument TEXT NOT NULL,
                    nemesis_response TEXT NOT NULL,
                    persuasion_delta INTEGER NOT NULL,
                    anger_delta INTEGER NOT NULL,
                    judge_reasoning TEXT NOT NULL,
                    argument_quality TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

    def create_game(self) -> GameState:
        now = datetime.now(timezone.utc)
        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO games (persuasion, anger, turn_count, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (0, 0, 0, GameStatus.ACTIVE.value, encode_dt(now), encode_dt(now)),
            )
            game_id = int(cursor.lastrowid)
            return GameState(
                id=game_id,
                persuasion=0,
                anger=0,
                turn_count=0,
                status=GameStatus.ACTIVE,
                created_at=now,
                updated_at=now,
            )

    def get_game(self, game_id: int) -> GameState | None:
        with self.connect() as connection:
            row = connection.execute("SELECT * FROM games WHERE id = ?", (game_id,)).fetchone()
        return self._game_from_row(row) if row else None

    def update_game(self, game: GameState) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                UPDATE games
                SET persuasion = ?, anger = ?, turn_count = ?, status = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    game.persuasion,
                    game.anger,
                    game.turn_count,
                    game.status.value,
                    encode_dt(game.updated_at),
                    game.id,
                ),
            )

    def add_turn(
        self,
        game: GameState,
        player_argument: str,
        nemesis_response: str,
        judgement: JudgeResult,
    ) -> Turn:
        now = datetime.now(timezone.utc)
        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO turns (
                    game_id, turn_number, player_argument, nemesis_response,
                    persuasion_delta, anger_delta, judge_reasoning, argument_quality, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    game.id,
                    game.turn_count,
                    player_argument,
                    nemesis_response,
                    judgement.persuasion_delta,
                    judgement.anger_delta,
                    judgement.reasoning,
                    judgement.argument_quality.value,
                    encode_dt(now),
                ),
            )
            turn_id = int(cursor.lastrowid)
        return Turn(
            id=turn_id,
            game_id=game.id,
            turn_number=game.turn_count,
            player_argument=player_argument,
            nemesis_response=nemesis_response,
            persuasion_delta=judgement.persuasion_delta,
            anger_delta=judgement.anger_delta,
            judge_reasoning=judgement.reasoning,
            argument_quality=judgement.argument_quality,
            created_at=now,
        )

    def list_turns(self, game_id: int) -> list[Turn]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM turns WHERE game_id = ? ORDER BY turn_number ASC, id ASC",
                (game_id,),
            ).fetchall()
        return [self._turn_from_row(row) for row in rows]

    def _game_from_row(self, row: sqlite3.Row) -> GameState:
        return GameState(
            id=row["id"],
            persuasion=row["persuasion"],
            anger=row["anger"],
            turn_count=row["turn_count"],
            status=GameStatus(row["status"]),
            created_at=decode_dt(row["created_at"]),
            updated_at=decode_dt(row["updated_at"]),
        )

    def _turn_from_row(self, row: sqlite3.Row) -> Turn:
        return Turn(
            id=row["id"],
            game_id=row["game_id"],
            turn_number=row["turn_number"],
            player_argument=row["player_argument"],
            nemesis_response=row["nemesis_response"],
            persuasion_delta=row["persuasion_delta"],
            anger_delta=row["anger_delta"],
            judge_reasoning=row["judge_reasoning"],
            argument_quality=ArgumentQuality(row["argument_quality"]),
            created_at=decode_dt(row["created_at"]),
        )
