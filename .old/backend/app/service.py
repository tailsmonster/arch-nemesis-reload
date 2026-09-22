import logging

from fastapi import HTTPException, status

from app.db import Database
from app.game_rules import apply_judgement, calculate_strike_delta
from app.llm.dry_run import generate_nemesis_response, judge_argument
from app.llm.workflow import run_turn_workflow
from app.models import (
    DebugJudgeResponse,
    DebugNemesisResponse,
    GameDetailResponse,
    GameListResponse,
    GameStatus,
    SubmitArgumentResponse,
    TurnPreviewResponse,
)


logger = logging.getLogger(__name__)


class GameService:
    def __init__(self, db: Database):
        self.db = db

    def create_game(self) -> GameDetailResponse:
        game, active_round = self.db.create_game()
        logger.info("Created game game_id=%s round_id=%s", game.id, active_round.id)
        return GameDetailResponse(
            game=game,
            active_round=active_round,
            turns=[],
            events=self.db.list_events(game.id, active_round.id),
        )

    def list_games(self) -> GameListResponse:
        return GameListResponse(games=self.db.list_games())

    def get_game(self, game_id: str) -> GameDetailResponse:
        game = self.db.get_game(game_id)
        if game is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
        active_round = self.db.get_round(game.active_round_id)
        if active_round is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Active round not found")
        return GameDetailResponse(
            game=game,
            active_round=active_round,
            turns=self.db.list_turns(game_id, active_round.id),
            events=self.db.list_events(game_id, active_round.id),
        )

    def list_turns(self, game_id: str):
        game = self.db.get_game(game_id)
        if game is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
        return self.db.list_turns(game_id, game.active_round_id)

    def submit_argument(self, game_id: str, argument: str) -> SubmitArgumentResponse:
        game = self.db.get_game(game_id)
        if game is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
        if game.status != GameStatus.ACTIVE:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Game is already complete")

        logger.info("Submitting turn game_id=%s round_id=%s", game.id, game.active_round_id)
        nemesis_response, judgement = run_turn_workflow(game, argument)
        updated_game = apply_judgement(game, judgement)
        strike_delta = calculate_strike_delta(judgement)
        self.db.update_game(updated_game)
        turn = self.db.add_turn(updated_game, argument, nemesis_response, judgement, strike_delta)
        self._record_turn_events(updated_game, turn.id, strike_delta)
        turns = self.db.list_turns(game_id, updated_game.active_round_id)
        return SubmitArgumentResponse(game=updated_game, turn=turn, turns=turns)

    def preview_turn(self, game_id: str, argument: str) -> TurnPreviewResponse:
        game = self.db.get_game(game_id)
        if game is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
        nemesis_response, judgement = run_turn_workflow(game, argument)
        preview_game = apply_judgement(game, judgement)
        return TurnPreviewResponse(
            game=game,
            preview_game=preview_game,
            nemesis_response=nemesis_response,
            judgement=judgement,
        )

    def debug_nemesis(self, game_id: str, argument: str) -> DebugNemesisResponse:
        game = self.db.get_game(game_id)
        if game is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
        return DebugNemesisResponse(nemesis_response=generate_nemesis_response(argument, game))

    def debug_judge(self, game_id: str, argument: str) -> DebugJudgeResponse:
        game = self.db.get_game(game_id)
        if game is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
        return DebugJudgeResponse(judgement=judge_argument(argument, game))

    def _record_turn_events(self, game, turn_id: str, strike_delta: int) -> None:
        if strike_delta > 0:
            self.db.add_event(
                game.id,
                "strike_added",
                "The Nemesis was offended. Strike added.",
                round_id=game.active_round_id,
                turn_id=turn_id,
            )
        if game.mode.value == "fight":
            self.db.add_event(
                game.id,
                "fight_ready",
                "The Nemesis is angry enough to trigger the future fight mode.",
                round_id=game.active_round_id,
                turn_id=turn_id,
            )
        if game.status != GameStatus.ACTIVE:
            self.db.add_event(
                game.id,
                f"game_{game.status.value}",
                f"Game ended with status: {game.status.value}.",
                round_id=game.active_round_id,
                turn_id=turn_id,
            )
