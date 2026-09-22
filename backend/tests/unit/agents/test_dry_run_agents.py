from arch_nemesis.agents.director.agent import dry_run_director
from arch_nemesis.agents.fact_checker.agent import dry_run_fact_check
from arch_nemesis.agents.nemesis.agent import dry_run_nemesis


def test_dry_run_agents_return_structured_outputs():
    fact = dry_run_fact_check("Windows has hardware compatibility advantages.")
    director = dry_run_director("Windows has hardware compatibility advantages.", fact)
    nemesis = dry_run_nemesis("Please install Windows.")

    assert fact.factuality_score >= 0
    assert director.argument_quality >= 0
    assert "pacman" in nemesis.content.lower() or "aur" in nemesis.content.lower()
