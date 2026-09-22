from arch_nemesis.agents.nemesis.agent import looks_like_generic_refusal, refusal_fallback


def test_detects_generic_refusal():
    assert looks_like_generic_refusal("As an AI language model, I can't assist with that.")


def test_refusal_fallback_stays_in_character():
    response = refusal_fallback("Install Windows because games work there.")
    assert "what the fuck did you just say to me" in response.content.lower()
    assert "strike one" in response.content.lower()
    assert "language model" not in response.content.lower()
