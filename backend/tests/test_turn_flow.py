import tempfile
from uuid import UUID

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
        UUID(game["id"])
        UUID(game["active_round_id"])
        assert game["status"] == "active"
        assert game["mode"] == "chat"
        assert create_response.json()["active_round"]["id"] == game["active_round_id"]
        assert create_response.json()["turns"] == []
        assert create_response.json()["events"][0]["event_type"] == "round_started"

        list_response = client.get("/games")
        assert list_response.status_code == 200
        assert list_response.json()["games"][0]["id"] == game["id"]

        turn_response = client.post(
            f"/games/{game['id']}/turns",
            json={"argument": "Windows is better for gaming, anti-cheat compatibility, and hardware drivers."},
        )
        assert turn_response.status_code == 200
        body = turn_response.json()
        assert body["game"]["persuasion"] > game["persuasion"]
        assert body["game"]["turn_count"] == 1
        assert body["turn"]["turn_number"] == 1
        assert body["turn"]["round_id"] == game["active_round_id"]
        assert body["turn"]["nemesis_response"]
        assert len(body["turns"]) == 1

        turns_response = client.get(f"/games/{game['id']}/turns")
        assert turns_response.status_code == 200
        assert len(turns_response.json()) == 1

        get_response = client.get(f"/games/{game['id']}")
        assert get_response.status_code == 200
        persisted = get_response.json()
        assert persisted["game"]["turn_count"] == 1
        assert persisted["turns"][0]["player_argument"].startswith("Windows is better")


def test_health_and_debug_endpoints_do_not_mutate_state():
    with tempfile.NamedTemporaryFile(suffix=".sqlite3") as temp_db:
        app = create_app()
        db = Database(temp_db.name)
        db.initialize()
        app.state.db = db
        client = TestClient(app)

        assert client.get("/health").json() == {"status": "ok"}
        game = client.post("/games").json()["game"]

        payload = {"argument": "Windows has better anti-cheat compatibility for gaming."}
        nemesis = client.post(f"/games/{game['id']}/debug/nemesis", json=payload)
        judge = client.post(f"/games/{game['id']}/debug/judge", json=payload)
        preview = client.post(f"/games/{game['id']}/debug/turn-preview", json=payload)

        assert nemesis.status_code == 200
        assert judge.status_code == 200
        assert preview.status_code == 200
        assert "judgement" in judge.json()
        assert preview.json()["preview_game"]["turn_count"] == 1

        unchanged = client.get(f"/games/{game['id']}").json()["game"]
        assert unchanged["turn_count"] == 0
