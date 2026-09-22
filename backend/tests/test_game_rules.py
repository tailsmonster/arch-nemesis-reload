from datetime import datetime, timezone

from app.game_rules import RuleConfig, apply_judgement
from app.models import ArgumentQuality, GameState, GameStatus, JudgeResult, PlayMode


def make_game(**overrides) -> GameState:
    now = datetime.now(timezone.utc)
    data = {
        "id": 1,
        "active_round_id": "round-1",
        "persuasion": 0,
        "anger": 0,
        "strikes": 0,
        "turn_count": 0,
        "status": GameStatus.ACTIVE,
        "mode": PlayMode.CHAT,
        "created_at": now,
        "updated_at": now,
    }
    data.update(overrides)
    return GameState(**data)


def make_judgement(persuasion_delta: int, anger_delta: int) -> JudgeResult:
    return JudgeResult(
        persuasion_delta=persuasion_delta,
        anger_delta=anger_delta,
        reasoning="test judgement",
        argument_quality=ArgumentQuality.OK,
    )


def test_apply_judgement_updates_state_deterministically():
    game = make_game(persuasion=5, anger=2, turn_count=1)

    updated = apply_judgement(game, make_judgement(3, 4))

    assert updated.persuasion == 8
    assert updated.anger == 6
    assert updated.turn_count == 2
    assert updated.status == GameStatus.ACTIVE


def test_apply_judgement_wins_at_persuasion_threshold():
    rules = RuleConfig(win_persuasion=10)
    game = make_game(persuasion=8)

    updated = apply_judgement(game, make_judgement(2, 0), rules)

    assert updated.status == GameStatus.WON


def test_apply_judgement_loses_at_anger_threshold():
    rules = RuleConfig(lose_anger=5)
    game = make_game(anger=4)

    updated = apply_judgement(game, make_judgement(0, 1), rules)

    assert updated.status == GameStatus.LOST


def test_completed_games_do_not_change():
    game = make_game(status=GameStatus.WON, persuasion=30, turn_count=3)

    updated = apply_judgement(game, make_judgement(-5, 10))

    assert updated == game


def test_offensive_judgement_adds_strike_and_sets_fight_mode():
    game = make_game()

    updated = apply_judgement(game, make_judgement(0, 5))

    assert updated.strikes == 1
    assert updated.mode == PlayMode.FIGHT
