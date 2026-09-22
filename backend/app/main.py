from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db import Database
from app.models import (
    DebugJudgeResponse,
    DebugNemesisResponse,
    GameDetailResponse,
    GameListResponse,
    HealthResponse,
    SubmitArgumentRequest,
    SubmitArgumentResponse,
    Turn,
    TurnPreviewResponse,
)
from app.service import GameService


def create_app() -> FastAPI:
    settings = get_settings()
    db = Database(settings.database_path)
    db.initialize()

    app = FastAPI(title="Arch Nemesis: Reload API")
    app.state.db = db

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def get_service() -> GameService:
        return GameService(app.state.db)

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok")

    @app.post("/games", response_model=GameDetailResponse)
    def create_game(service: GameService = Depends(get_service)) -> GameDetailResponse:
        return service.create_game()

    @app.get("/games", response_model=GameListResponse)
    def list_games(service: GameService = Depends(get_service)) -> GameListResponse:
        return service.list_games()

    @app.get("/games/{game_id}", response_model=GameDetailResponse)
    def get_game(game_id: str, service: GameService = Depends(get_service)) -> GameDetailResponse:
        return service.get_game(game_id)

    @app.get("/games/{game_id}/turns", response_model=list[Turn])
    def list_turns(game_id: str, service: GameService = Depends(get_service)) -> list[Turn]:
        return service.list_turns(game_id)

    @app.post("/games/{game_id}/turns", response_model=SubmitArgumentResponse)
    def submit_turn(
        game_id: str,
        request: SubmitArgumentRequest,
        service: GameService = Depends(get_service),
    ) -> SubmitArgumentResponse:
        return service.submit_argument(game_id, request.argument)

    @app.post("/games/{game_id}/debug/nemesis", response_model=DebugNemesisResponse)
    def debug_nemesis(
        game_id: str,
        request: SubmitArgumentRequest,
        service: GameService = Depends(get_service),
    ) -> DebugNemesisResponse:
        return service.debug_nemesis(game_id, request.argument)

    @app.post("/games/{game_id}/debug/judge", response_model=DebugJudgeResponse)
    def debug_judge(
        game_id: str,
        request: SubmitArgumentRequest,
        service: GameService = Depends(get_service),
    ) -> DebugJudgeResponse:
        return service.debug_judge(game_id, request.argument)

    @app.post("/games/{game_id}/debug/turn-preview", response_model=TurnPreviewResponse)
    def preview_turn(
        game_id: str,
        request: SubmitArgumentRequest,
        service: GameService = Depends(get_service),
    ) -> TurnPreviewResponse:
        return service.preview_turn(game_id, request.argument)

    return app


app = create_app()
