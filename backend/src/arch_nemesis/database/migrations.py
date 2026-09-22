from arch_nemesis.database.connection import get_connection


SCHEMA = """
CREATE TABLE IF NOT EXISTS games (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    persuasion INTEGER NOT NULL DEFAULT 0,
    anger INTEGER NOT NULL DEFAULT 0,
    turn_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS turns (
    id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    player_message_id TEXT NOT NULL REFERENCES messages(id),
    nemesis_message_id TEXT REFERENCES messages(id),
    turn_number INTEGER NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evaluations (
    id TEXT PRIMARY KEY,
    turn_id TEXT NOT NULL REFERENCES turns(id) ON DELETE CASCADE,
    fact_check TEXT NOT NULL,
    argument_quality INTEGER NOT NULL,
    persuasion_delta INTEGER NOT NULL,
    anger_delta INTEGER NOT NULL,
    reason TEXT NOT NULL,
    raw_output TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS llm_runs (
    id TEXT PRIMARY KEY,
    game_id TEXT,
    turn_id TEXT,
    agent_name TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    prompt_hash TEXT NOT NULL,
    latency_ms INTEGER NOT NULL,
    success INTEGER NOT NULL,
    error TEXT,
    response_preview TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS graph_runs (
    id TEXT PRIMARY KEY,
    game_id TEXT,
    turn_id TEXT,
    status TEXT NOT NULL,
    nodes_visited TEXT NOT NULL,
    error TEXT,
    created_at TEXT NOT NULL,
    completed_at TEXT
);
"""


def initialize_database() -> None:
    with get_connection() as connection:
        connection.executescript(SCHEMA)
