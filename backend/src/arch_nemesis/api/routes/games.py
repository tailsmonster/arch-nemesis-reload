from fastapi import APIRouter, HTTPException

from arch_nemesis.api.schemas.games import CreateGameRequest, GameDetailResponse, GameResponse
from arch_nemesis.services import game_service

router = APIRouter()


@router.post("", response_model=GameDetailResponse)
def create_game(request: CreateGameRequest) -> dict:
    return game_service.create_game(request.title)


@router.get("", response_model=list[GameResponse])
def list_games() -> list[dict]:
    return game_service.list_games()


@router.get("/{game_id}", response_model=GameDetailResponse)
def get_game(game_id: str) -> dict:
    game = game_service.get_game_detail(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game
