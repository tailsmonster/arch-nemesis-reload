from arch_nemesis.agents.director.models import DirectorEvaluation
from arch_nemesis.game.rules import apply_director_evaluation


def test_apply_director_evaluation_clamps_deltas():
    evaluation = DirectorEvaluation(
        intent="test",
        argument_quality=10,
        persuasion_delta=10,
        anger_delta=-10,
        reason="test",
    )
    result = apply_director_evaluation(evaluation)
    assert result.persuasion_delta == 10
    assert result.anger_delta == -10
