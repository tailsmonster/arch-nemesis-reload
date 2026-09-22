from fastapi.testclient import TestClient

from arch_nemesis.main import app


def test_health_endpoint(monkeypatch, tmp_path):
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "test.sqlite3"))
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["database"] == "ok"


def test_llm_health_endpoint():
    client = TestClient(app)
    response = client.get("/api/health/llm")
    assert response.status_code == 200
    assert "provider" in response.json()
