from arch_nemesis.agents.nemesis.agent import dry_run_nemesis, looks_like_generic_refusal, refusal_fallback
from arch_nemesis.agents.nemesis.models import NemesisResponse
from arch_nemesis.config import get_settings
from arch_nemesis.game.models import RuleApplication
from arch_nemesis.llm.factory import get_llm_client
from arch_nemesis.llm.tracing import trace_llm_result
from arch_nemesis.prompts.loader import load_prompt


def respond(argument: str, game: dict, rules: RuleApplication, game_id: str | None = None) -> NemesisResponse:
    if get_settings().dry_run_mode:
        return dry_run_nemesis(argument)
    personality = load_prompt("nemesis/personality.txt")
    system = load_prompt("nemesis/system.txt")
    template = load_prompt("nemesis/response.txt")
    prompt = f"{personality.text}\n\n{system.text}\n\n" + template.text.format(
        persuasion=game["persuasion"],
        anger=game["anger"],
        turn_count=game["turn_count"],
        argument=argument,
        reason=rules.reason,
    )
    result = get_llm_client().complete(prompt, template.sha256, "nemesis")
    trace_llm_result("nemesis", result, game_id=game_id)
    if looks_like_generic_refusal(result.text):
        return refusal_fallback(argument)
    return NemesisResponse(content=result.text)
