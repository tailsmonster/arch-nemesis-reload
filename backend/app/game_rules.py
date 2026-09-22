from dataclasses import dataclass
from datetime import datetime, timezone

from app.models import GameState, GameStatus, JudgeResult


@dataclass(frozen=True)
class RuleConfig:
    initial_persuasion: int = 0
    initial_anger: int = 0
    initial_turn_count: int = 0
    min_persuasion: int = 0
    max_persuasion: int = 100
    min_anger: int = 0
    max_anger: int = 100
    win_persuasion: int = 30
    lose_anger: int = 30
    max_turns: int = 10


DEFAULT_RULES = RuleConfig()


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def new_game_state(game_id: int, rules: RuleConfig = DEFAULT_RULES) -> GameState:
    now = now_utc()
    return GameState(
        id=game_id,
        persuasion=rules.initial_persuasion,
        anger=rules.initial_anger,
        turn_count=rules.initial_turn_count,
        status=GameStatus.ACTIVE,
        created_at=now,
        updated_at=now,
    )


def clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))


def apply_judgement(
    game: GameState,
    judgement: JudgeResult,
    rules: RuleConfig = DEFAULT_RULES,
) -> GameState:
    if game.status != GameStatus.ACTIVE:
        return game

    persuasion = clamp(
        game.persuasion + judgement.persuasion_delta,
        rules.min_persuasion,
        rules.max_persuasion,
    )
    anger = clamp(game.anger + judgement.anger_delta, rules.min_anger, rules.max_anger)
    turn_count = game.turn_count + 1

    status = GameStatus.ACTIVE
    if persuasion >= rules.win_persuasion:
        status = GameStatus.WON
    elif anger >= rules.lose_anger or turn_count >= rules.max_turns:
        status = GameStatus.LOST

    return game.model_copy(
        update={
            "persuasion": persuasion,
            "anger": anger,
            "turn_count": turn_count,
            "status": status,
            "updated_at": now_utc(),
        }
    )
