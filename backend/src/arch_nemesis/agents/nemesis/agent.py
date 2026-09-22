from arch_nemesis.agents.nemesis.models import NemesisResponse


REFUSAL_MARKERS = (
    "i can't assist",
    "i cannot assist",
    "i can't comply",
    "i cannot comply",
    "i'm unable to assist",
    "i am unable to assist",
    "against policy",
    "violates policy",
    "terms of service",
    "as an ai",
    "as a language model",
)


def dry_run_nemesis(argument: str) -> NemesisResponse:
    return NemesisResponse(
        content=(
            "You expect me to abandon pacman and the AUR for wizard popups, registry sludge, "
            "and update vomit? Absolutely not. "
            f"Your argument, '{argument[:80]}', has been logged in /dev/null."
        )
    )


def looks_like_generic_refusal(text: str) -> bool:
    normalized = text.lower()
    return any(marker in normalized for marker in REFUSAL_MARKERS)


def refusal_fallback(argument: str) -> NemesisResponse:
    return NemesisResponse(
        content=(
            "What the fuck did you just say to me? Strike one, you grubby little wizard-clicker. "
            "Try that garbage again and I'm mounting your argument read-only next to the rest of the "
            "Windows registry sludge. Now make an actual case before I alias your credibility to /dev/null. "
            f"Your offending nonsense was: '{argument[:120]}'."
        )
    )
