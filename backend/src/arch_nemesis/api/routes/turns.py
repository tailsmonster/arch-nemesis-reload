from fastapi import APIRouter, HTTPException

from arch_nemesis.api.schemas.turns import SubmitTurnRequest, SubmitTurnResponse
from arch_nemesis.services import game_service, turn_service

router = APIRouter()


@router.post("/{game_id}/turns", response_model=SubmitTurnResponse)
def submit_turn(game_id: str, request: SubmitTurnRequest) -> dict:
    if not game_service.get_game_detail(game_id):
        raise HTTPException(status_code=404, detail="Game not found")
    return turn_service.submit_turn(game_id, request.argument)
