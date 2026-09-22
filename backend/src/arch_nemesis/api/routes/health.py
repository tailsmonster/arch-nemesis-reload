from fastapi import APIRouter

from arch_nemesis.config import get_settings
from arch_nemesis.database.connection import get_connection

router = APIRouter()


@router.get("/health")
def health() -> dict:
    with get_connection() as connection:
        connection.execute("SELECT 1").fetchone()
    return {"status": "ok", "database": "ok"}


@router.get("/health/llm")
def llm_health() -> dict:
    settings = get_settings()
    configured = settings.dry_run_mode or bool(settings.openai_api_key)
    return {
        "status": "ok" if configured else "missing_api_key",
        "provider": "dry-run" if settings.dry_run_mode else settings.llm_provider,
        "model": "deterministic-harness" if settings.dry_run_mode else settings.llm_model,
        "dry_run_mode": settings.dry_run_mode,
        "configured": configured,
    }
