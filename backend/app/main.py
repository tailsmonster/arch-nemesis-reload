from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db import Database
from app.models import GameDetailResponse, SubmitArgumentRequest, SubmitArgumentResponse
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

    @app.post("/games", response_model=GameDetailResponse)
    def create_game(service: GameService = Depends(get_service)) -> GameDetailResponse:
        return service.create_game()

    @app.get("/games/{game_id}", response_model=GameDetailResponse)
    def get_game(game_id: int, service: GameService = Depends(get_service)) -> GameDetailResponse:
        return service.get_game(game_id)

    @app.post("/games/{game_id}/turns", response_model=SubmitArgumentResponse)
    def submit_turn(
        game_id: int,
        request: SubmitArgumentRequest,
        service: GameService = Depends(get_service),
    ) -> SubmitArgumentResponse:
        return service.submit_argument(game_id, request.argument)

    return app


app = create_app()
