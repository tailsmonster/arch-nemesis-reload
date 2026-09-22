from arch_nemesis.agents.director.agent import dry_run_director, parse_director_output
from arch_nemesis.agents.director.models import DirectorEvaluation
from arch_nemesis.agents.fact_checker.models import FactCheckResult
from arch_nemesis.config import get_settings
from arch_nemesis.llm.factory import get_llm_client
from arch_nemesis.llm.tracing import trace_llm_result
from arch_nemesis.prompts.loader import load_prompt


def evaluate_turn(
    argument: str, game: dict, fact_check: FactCheckResult, game_id: str | None = None
) -> DirectorEvaluation:
    if get_settings().dry_run_mode:
        return dry_run_director(argument, fact_check)
    system = load_prompt("director/system.txt")
    prompt_template = load_prompt("director/evaluate_turn.txt")
    prompt = f"{system.text}\n\n" + prompt_template.text.format(
        persuasion=game["persuasion"],
        anger=game["anger"],
        turn_count=game["turn_count"],
        argument=argument,
        fact_check=fact_check.model_dump_json(),
    )
    result = get_llm_client().complete(prompt, prompt_template.sha256, "director")
    trace_llm_result("director", result, game_id=game_id)
    return parse_director_output(result.text)
