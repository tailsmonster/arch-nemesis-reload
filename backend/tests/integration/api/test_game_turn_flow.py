from fastapi.testclient import TestClient

from arch_nemesis.config import get_settings
from arch_nemesis.database.migrations import initialize_database
from arch_nemesis.main import app


def test_game_turn_flow(monkeypatch, tmp_path):
    monkeypatch.setenv("DRY_RUN_MODE", "true")
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "test.sqlite3"))
    get_settings.cache_clear()
    initialize_database()
    client = TestClient(app)

    created = client.post("/api/games", json={"title": "Test Game"})
    assert created.status_code == 200
    game_id = created.json()["id"]

    turn = client.post(
        f"/api/games/{game_id}/turns",
        json={"argument": "Windows has strong compatibility for commercial games."},
    )
    assert turn.status_code == 200
    body = turn.json()
    assert body["game"]["turn_count"] == 1
    assert body["turn"]["game_id"] == game_id
