from arch_nemesis.agents.director.models import DirectorEvaluation
from arch_nemesis.game.models import RuleApplication
from arch_nemesis.game.scoring import clamp_delta


def apply_director_evaluation(evaluation: DirectorEvaluation) -> RuleApplication:
    return RuleApplication(
        persuasion_delta=clamp_delta(evaluation.persuasion_delta),
        anger_delta=clamp_delta(evaluation.anger_delta),
        reason=evaluation.reason,
    )
