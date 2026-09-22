from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationRecord:
    id: str
    turn_id: str
    fact_check: str
    argument_quality: int
    persuasion_delta: int
    anger_delta: int
    reason: str
    raw_output: str
    created_at: str
