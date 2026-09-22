from arch_nemesis.agents.director.models import DirectorEvaluation
from arch_nemesis.agents.fact_checker.models import FactCheckResult


def parse_director_output(text: str) -> DirectorEvaluation:
    try:
        return DirectorEvaluation.model_validate_json(text)
    except Exception:
        return DirectorEvaluation(
            intent="unknown",
            argument_quality=5,
            persuasion_delta=1,
            anger_delta=1,
            reason="Model output was not valid JSON; fallback evaluation applied.",
        )


def dry_run_director(argument: str, fact_check: FactCheckResult) -> DirectorEvaluation:
    quality = min(10, max(1, fact_check.factuality_score))
    persuasion_delta = 3 if quality >= 7 else 1
    anger_delta = 2 if "windows" in argument.lower() else 1
    return DirectorEvaluation(
        intent="persuade_with_pragmatism",
        argument_quality=quality,
        persuasion_delta=persuasion_delta,
        anger_delta=anger_delta,
        reason="Deterministic director harness result.",
    )
