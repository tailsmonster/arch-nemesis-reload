import tempfile

from fastapi.testclient import TestClient

from app.db import Database
from app.main import create_app


def test_create_submit_and_retrieve_game_turn_flow():
    with tempfile.NamedTemporaryFile(suffix=".sqlite3") as temp_db:
        app = create_app()
        db = Database(temp_db.name)
        db.initialize()
        app.state.db = db

        client = TestClient(app)

        create_response = client.post("/games")
        assert create_response.status_code == 200
        game = create_response.json()["game"]
        assert game["status"] == "active"
        assert create_response.json()["turns"] == []

        turn_response = client.post(
            f"/games/{game['id']}/turns",
            json={"argument": "Windows is better for gaming, anti-cheat compatibility, and hardware drivers."},
        )
        assert turn_response.status_code == 200
        body = turn_response.json()
        assert body["game"]["persuasion"] > game["persuasion"]
        assert body["game"]["turn_count"] == 1
        assert body["turn"]["turn_number"] == 1
        assert body["turn"]["nemesis_response"]
        assert len(body["turns"]) == 1

        get_response = client.get(f"/games/{game['id']}")
        assert get_response.status_code == 200
        persisted = get_response.json()
        assert persisted["game"]["turn_count"] == 1
        assert persisted["turns"][0]["player_argument"].startswith("Windows is better")
