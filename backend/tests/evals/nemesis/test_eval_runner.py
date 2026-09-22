from pathlib import Path

from arch_nemesis.evals.runner import run_seed_evals


def test_eval_runner_smoke(tmp_path: Path):
    dataset = tmp_path / "cases.jsonl"
    dataset.write_text('{"id":"case-1","argument":"Windows runs my game."}\n', encoding="utf-8")
    results = run_seed_evals(dataset)
    assert len(results) == 1
    assert "rubric" in results[0]
