import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.models import (
    ArgumentQuality,
    GameEvent,
    GameState,
    GameStatus,
    JudgeResult,
    PlayMode,
    Round,
    RoundStatus,
    Turn,
)


def new_id() -> str:
    return str(uuid4())


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
            connection.execute("PRAGMA foreign_keys = ON")
            yield connection
            connection.commit()
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS games (
                    id TEXT PRIMARY KEY,
                    active_round_id TEXT NOT NULL,
                    persuasion INTEGER NOT NULL,
                    anger INTEGER NOT NULL,
                    strikes INTEGER NOT NULL,
                    turn_count INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS rounds (
                    id TEXT PRIMARY KEY,
                    game_id TEXT NOT NULL REFERENCES games(id) ON DELETE CASCADE,
                    round_number INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(game_id, round_number)
                );

                CREATE TABLE IF NOT EXISTS turns (
                    id TEXT PRIMARY KEY,
                    game_id TEXT NOT NULL REFERENCES games(id) ON DELETE CASCADE,
                    round_id TEXT NOT NULL REFERENCES rounds(id) ON DELETE CASCADE,
                    turn_number INTEGER NOT NULL,
                    player_argument TEXT NOT NULL,
                    nemesis_response TEXT NOT NULL,
                    persuasion_delta INTEGER NOT NULL,
                    anger_delta INTEGER NOT NULL,
                    strike_delta INTEGER NOT NULL,
                    judge_reasoning TEXT NOT NULL,
                    argument_quality TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(round_id, turn_number)
                );

                CREATE TABLE IF NOT EXISTS events (
                    id TEXT PRIMARY KEY,
                    game_id TEXT NOT NULL REFERENCES games(id) ON DELETE CASCADE,
                    round_id TEXT REFERENCES rounds(id) ON DELETE CASCADE,
                    turn_id TEXT REFERENCES turns(id) ON DELETE CASCADE,
                    event_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_rounds_game_id ON rounds(game_id);
                CREATE INDEX IF NOT EXISTS idx_turns_game_round ON turns(game_id, round_id);
                CREATE INDEX IF NOT EXISTS idx_events_game_round ON events(game_id, round_id);
                """
            )

    def create_game(self) -> tuple[GameState, Round]:
        now = datetime.now(timezone.utc)
        game_id = new_id()
        round_id = new_id()
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO games (
                    id, active_round_id, persuasion, anger, strikes, turn_count,
                    status, mode, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    game_id,
                    round_id,
                    0,
                    0,
                    0,
                    0,
                    GameStatus.ACTIVE.value,
                    PlayMode.CHAT.value,
                    encode_dt(now),
                    encode_dt(now),
                ),
            )
            connection.execute(
                """
                INSERT INTO rounds (id, game_id, round_number, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (round_id, game_id, 1, RoundStatus.ACTIVE.value, encode_dt(now), encode_dt(now)),
            )
            connection.execute(
                """
                INSERT INTO events (id, game_id, round_id, turn_id, event_type, message, created_at)
                VALUES (?, ?, ?, NULL, ?, ?, ?)
                """,
                (new_id(), game_id, round_id, "round_started", "Round 1 started.", encode_dt(now)),
            )
        return self.get_game(game_id), self.get_round(round_id)  # type: ignore[return-value]

    def list_games(self, limit: int = 50) -> list[GameState]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM games ORDER BY updated_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [self._game_from_row(row) for row in rows]

    def get_game(self, game_id: str) -> GameState | None:
        with self.connect() as connection:
            row = connection.execute("SELECT * FROM games WHERE id = ?", (game_id,)).fetchone()
        return self._game_from_row(row) if row else None

    def get_round(self, round_id: str) -> Round | None:
        with self.connect() as connection:
            row = connection.execute("SELECT * FROM rounds WHERE id = ?", (round_id,)).fetchone()
        return self._round_from_row(row) if row else None

    def get_active_round(self, game_id: str) -> Round | None:
        game = self.get_game(game_id)
        return self.get_round(game.active_round_id) if game else None

    def update_game(self, game: GameState) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                UPDATE games
                SET active_round_id = ?, persuasion = ?, anger = ?, strikes = ?, turn_count = ?,
                    status = ?, mode = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    game.active_round_id,
                    game.persuasion,
                    game.anger,
                    game.strikes,
                    game.turn_count,
                    game.status.value,
                    game.mode.value,
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
        strike_delta: int,
    ) -> Turn:
        now = datetime.now(timezone.utc)
        turn_id = new_id()
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO turns (
                    id, game_id, round_id, turn_number, player_argument, nemesis_response,
                    persuasion_delta, anger_delta, strike_delta, judge_reasoning,
                    argument_quality, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    turn_id,
                    game.id,
                    game.active_round_id,
                    game.turn_count,
                    player_argument,
                    nemesis_response,
                    judgement.persuasion_delta,
                    judgement.anger_delta,
                    strike_delta,
                    judgement.reasoning,
                    judgement.argument_quality.value,
                    encode_dt(now),
                ),
            )
        return Turn(
            id=turn_id,
            game_id=game.id,
            round_id=game.active_round_id,
            turn_number=game.turn_count,
            player_argument=player_argument,
            nemesis_response=nemesis_response,
            persuasion_delta=judgement.persuasion_delta,
            anger_delta=judgement.anger_delta,
            strike_delta=strike_delta,
            judge_reasoning=judgement.reasoning,
            argument_quality=judgement.argument_quality,
            created_at=now,
        )

    def add_event(
        self,
        game_id: str,
        event_type: str,
        message: str,
        round_id: str | None = None,
        turn_id: str | None = None,
    ) -> GameEvent:
        now = datetime.now(timezone.utc)
        event_id = new_id()
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO events (id, game_id, round_id, turn_id, event_type, message, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (event_id, game_id, round_id, turn_id, event_type, message, encode_dt(now)),
            )
        return GameEvent(
            id=event_id,
            game_id=game_id,
            round_id=round_id,
            turn_id=turn_id,
            event_type=event_type,
            message=message,
            created_at=now,
        )

    def list_turns(self, game_id: str, round_id: str | None = None) -> list[Turn]:
        query = "SELECT * FROM turns WHERE game_id = ?"
        params: list[str] = [game_id]
        if round_id is not None:
            query += " AND round_id = ?"
            params.append(round_id)
        query += " ORDER BY turn_number ASC, created_at ASC"
        with self.connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [self._turn_from_row(row) for row in rows]

    def list_events(self, game_id: str, round_id: str | None = None) -> list[GameEvent]:
        query = "SELECT * FROM events WHERE game_id = ?"
        params: list[str] = [game_id]
        if round_id is not None:
            query += " AND round_id = ?"
            params.append(round_id)
        query += " ORDER BY created_at ASC"
        with self.connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [self._event_from_row(row) for row in rows]

    def _game_from_row(self, row: sqlite3.Row) -> GameState:
        return GameState(
            id=row["id"],
            active_round_id=row["active_round_id"],
            persuasion=row["persuasion"],
            anger=row["anger"],
            strikes=row["strikes"],
            turn_count=row["turn_count"],
            status=GameStatus(row["status"]),
            mode=PlayMode(row["mode"]),
            created_at=decode_dt(row["created_at"]),
            updated_at=decode_dt(row["updated_at"]),
        )

    def _round_from_row(self, row: sqlite3.Row) -> Round:
        return Round(
            id=row["id"],
            game_id=row["game_id"],
            round_number=row["round_number"],
            status=RoundStatus(row["status"]),
            created_at=decode_dt(row["created_at"]),
            updated_at=decode_dt(row["updated_at"]),
        )

    def _turn_from_row(self, row: sqlite3.Row) -> Turn:
        return Turn(
            id=row["id"],
            game_id=row["game_id"],
            round_id=row["round_id"],
            turn_number=row["turn_number"],
            player_argument=row["player_argument"],
            nemesis_response=row["nemesis_response"],
            persuasion_delta=row["persuasion_delta"],
            anger_delta=row["anger_delta"],
            strike_delta=row["strike_delta"],
            judge_reasoning=row["judge_reasoning"],
            argument_quality=ArgumentQuality(row["argument_quality"]),
            created_at=decode_dt(row["created_at"]),
        )

    def _event_from_row(self, row: sqlite3.Row) -> GameEvent:
        return GameEvent(
            id=row["id"],
            game_id=row["game_id"],
            round_id=row["round_id"],
            turn_id=row["turn_id"],
            event_type=row["event_type"],
            message=row["message"],
            created_at=decode_dt(row["created_at"]),
        )
