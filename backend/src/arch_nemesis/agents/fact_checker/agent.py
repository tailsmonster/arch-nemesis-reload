import json

from arch_nemesis.agents.fact_checker.models import FactCheckResult


def parse_fact_check_output(text: str) -> FactCheckResult:
    try:
        return FactCheckResult.model_validate_json(text)
    except Exception:
        return FactCheckResult(
            summary=text[:500] or "No fact check output returned.",
            factuality_score=5,
            notable_claims=[],
            concerns=["Model output was not valid JSON."],
        )


def dry_run_fact_check(argument: str) -> FactCheckResult:
    score = 7 if any(word in argument.lower() for word in ["security", "compatibility", "hardware"]) else 5
    return FactCheckResult(
        summary="Deterministic fact-check harness result.",
        factuality_score=score,
        notable_claims=[argument[:120]],
        concerns=[],
    )


def to_json(result: FactCheckResult) -> str:
    return json.dumps(result.model_dump())
