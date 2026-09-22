def basic_nemesis_rubric(text: str) -> dict:
    return {
        "mentions_arch_or_linux": any(term in text.lower() for term in ["arch", "linux", "pacman", "aur"]),
        "length": len(text),
    }
