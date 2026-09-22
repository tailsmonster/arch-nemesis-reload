import json
from pathlib import Path

from arch_nemesis.agents.nemesis.agent import dry_run_nemesis
from arch_nemesis.evals.rubrics import basic_nemesis_rubric


def run_seed_evals(dataset_path: Path) -> list[dict]:
    results = []
    for line in dataset_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        case = json.loads(line)
        response = dry_run_nemesis(case["argument"])
        results.append({"case": case, "response": response.content, "rubric": basic_nemesis_rubric(response.content)})
    return results


def main() -> None:
    dataset = Path("evals/datasets/seed_arguments.jsonl")
    print(json.dumps(run_seed_evals(dataset), indent=2))


if __name__ == "__main__":
    main()
