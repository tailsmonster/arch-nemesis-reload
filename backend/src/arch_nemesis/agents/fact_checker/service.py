from arch_nemesis.agents.fact_checker.agent import dry_run_fact_check, parse_fact_check_output
from arch_nemesis.agents.fact_checker.models import FactCheckResult
from arch_nemesis.config import get_settings
from arch_nemesis.llm.factory import get_llm_client
from arch_nemesis.llm.tracing import trace_llm_result
from arch_nemesis.prompts.loader import load_prompt


def fact_check(argument: str, game_id: str | None = None) -> FactCheckResult:
    if get_settings().dry_run_mode:
        return dry_run_fact_check(argument)
    system = load_prompt("fact_checker/system.txt")
    prompt_template = load_prompt("fact_checker/fact_check.txt")
    prompt = f"{system.text}\n\n{prompt_template.text.format(argument=argument)}"
    result = get_llm_client().complete(prompt, prompt_template.sha256, "fact_checker")
    trace_llm_result("fact_checker", result, game_id=game_id)
    return parse_fact_check_output(result.text)
