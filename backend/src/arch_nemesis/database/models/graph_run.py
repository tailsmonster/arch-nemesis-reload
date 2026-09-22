from dataclasses import dataclass


@dataclass(frozen=True)
class GraphRunRecord:
    id: str
    status: str
    nodes_visited: str
    created_at: str
    completed_at: str | None
