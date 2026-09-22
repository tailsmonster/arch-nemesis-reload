import logging
from dataclasses import dataclass
from datetime import datetime, timezone

from app.models import GameState, GameStatus, JudgeResult, PlayMode


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RuleConfig:
    initial_persuasion: int = 0
    initial_anger: int = 0
    initial_strikes: int = 0
    initial_turn_count: int = 0
    min_persuasion: int = 0
    max_persuasion: int = 100
    min_anger: int = 0
    max_anger: int = 100
    win_persuasion: int = 30
    lose_anger: int = 30
    fight_anger: int = 35
    lose_strikes: int = 3
    max_turns: int = 10


DEFAULT_RULES = RuleConfig()


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def new_game_state(game_id: str, round_id: str, rules: RuleConfig = DEFAULT_RULES) -> GameState:
    now = now_utc()
    return GameState(
        id=game_id,
        active_round_id=round_id,
        persuasion=rules.initial_persuasion,
        anger=rules.initial_anger,
        strikes=rules.initial_strikes,
        turn_count=rules.initial_turn_count,
        status=GameStatus.ACTIVE,
        mode=PlayMode.CHAT,
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

    logger.info(
        "Applying judgement game_id=%s persuasion_delta=%s anger_delta=%s quality=%s",
        game.id,
        judgement.persuasion_delta,
        judgement.anger_delta,
        judgement.argument_quality,
    )

    persuasion = clamp(
        game.persuasion + judgement.persuasion_delta,
        rules.min_persuasion,
        rules.max_persuasion,
    )
    anger = clamp(game.anger + judgement.anger_delta, rules.min_anger, rules.max_anger)
    strike_delta = calculate_strike_delta(judgement)
    strikes = game.strikes + strike_delta
    turn_count = game.turn_count + 1

    status = GameStatus.ACTIVE
    mode = PlayMode.CHAT
    if persuasion >= rules.win_persuasion:
        status = GameStatus.WON
        mode = PlayMode.COMPLETE
    elif anger >= rules.lose_anger or strikes >= rules.lose_strikes or turn_count >= rules.max_turns:
        status = GameStatus.LOST
        mode = PlayMode.COMPLETE
    elif anger >= rules.fight_anger or strikes > 0:
        mode = PlayMode.FIGHT

    return game.model_copy(
        update={
            "persuasion": persuasion,
            "anger": anger,
            "strikes": strikes,
            "turn_count": turn_count,
            "status": status,
            "mode": mode,
            "updated_at": now_utc(),
        }
    )


def calculate_strike_delta(judgement: JudgeResult) -> int:
    return 1 if judgement.anger_delta >= 5 and judgement.persuasion_delta <= 1 else 0
