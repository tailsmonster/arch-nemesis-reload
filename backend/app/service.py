from fastapi import HTTPException, status

from app.db import Database
from app.game_rules import apply_judgement
from app.llm.workflow import run_turn_workflow
from app.models import GameDetailResponse, GameStatus, SubmitArgumentResponse


class GameService:
    def __init__(self, db: Database):
        self.db = db

    def create_game(self) -> GameDetailResponse:
        game = self.db.create_game()
        return GameDetailResponse(game=game, turns=[])

    def get_game(self, game_id: int) -> GameDetailResponse:
        game = self.db.get_game(game_id)
        if game is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
        return GameDetailResponse(game=game, turns=self.db.list_turns(game_id))

    def submit_argument(self, game_id: int, argument: str) -> SubmitArgumentResponse:
        game = self.db.get_game(game_id)
        if game is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
        if game.status != GameStatus.ACTIVE:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Game is already complete")

        nemesis_response, judgement = run_turn_workflow(game, argument)
        updated_game = apply_judgement(game, judgement)
        self.db.update_game(updated_game)
        turn = self.db.add_turn(updated_game, argument, nemesis_response, judgement)
        turns = self.db.list_turns(game_id)
        return SubmitArgumentResponse(game=updated_game, turn=turn, turns=turns)
