from app.models import ArgumentQuality, GameState, JudgeResult


def generate_nemesis_response(argument: str, game: GameState) -> str:
    lower = argument.lower()
    if "game" in lower or "proton" in lower or "steam" in lower:
        return (
            "Gaming? Please. I compile kernels between matches. Still, I admit "
            "not every anti-cheat vendor worships at the altar of Tux."
        )
    if "work" in lower or "office" in lower or "compatibility" in lower:
        return (
            "Compatibility is what people say when they fear editing config files. "
            "But yes, your corporate spreadsheet prison probably expects Windows."
        )
    if "hardware" in lower or "driver" in lower:
        return (
            "Drivers are just puzzles for the worthy. Unfortunately, some hardware "
            "vendors do seem determined to make Linux users solve riddles forever."
        )
    return (
        "I use Arch, by the way. Your argument has been received, filed under "
        "things a package manager could have solved better."
    )


def judge_argument(argument: str, game: GameState) -> JudgeResult:
    lower = argument.lower()
    persuasion_delta = 1
    anger_delta = 1
    reasons: list[str] = ["The argument was understandable but not yet devastating."]

    persuasive_terms = ["gaming", "game", "driver", "hardware", "compatibility", "office", "adobe", "anti-cheat"]
    inflammatory_terms = ["arch sucks", "linux sucks", "idiot", "fanboy", "cult"]

    matches = sum(1 for term in persuasive_terms if term in lower)
    if matches >= 2:
        persuasion_delta = 6
        anger_delta = 2
        quality = ArgumentQuality.STRONG
        reasons = ["The argument names concrete compatibility or software pain points."]
    elif matches == 1:
        persuasion_delta = 3
        anger_delta = 1
        quality = ArgumentQuality.OK
        reasons = ["The argument has one practical point the Nemesis cannot fully dismiss."]
    else:
        quality = ArgumentQuality.WEAK

    if any(term in lower for term in inflammatory_terms):
        anger_delta += 4
        persuasion_delta = max(0, persuasion_delta - 2)
        reasons.append("Insults made the Nemesis defensive.")

    if len(argument.split()) >= 25:
        persuasion_delta += 1
        reasons.append("The argument included enough detail to feel considered.")

    return JudgeResult(
        persuasion_delta=persuasion_delta,
        anger_delta=anger_delta,
        reasoning=" ".join(reasons),
        argument_quality=quality,
    )
