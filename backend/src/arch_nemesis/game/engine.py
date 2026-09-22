from arch_nemesis.agents.director.models import DirectorEvaluation
from arch_nemesis.game.rules import apply_director_evaluation


def evaluate_game_impact(evaluation: DirectorEvaluation):
    return apply_director_evaluation(evaluation)
