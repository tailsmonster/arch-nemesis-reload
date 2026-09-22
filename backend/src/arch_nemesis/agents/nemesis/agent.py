from arch_nemesis.agents.nemesis.models import NemesisResponse


def dry_run_nemesis(argument: str) -> NemesisResponse:
    return NemesisResponse(
        content=(
            "You expect me to abandon pacman and the AUR for wizard popups? "
            f"Your argument, '{argument[:80]}', has been logged in /dev/null."
        )
    )
