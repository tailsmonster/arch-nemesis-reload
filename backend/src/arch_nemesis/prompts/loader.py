from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path


PROMPT_ROOT = Path(__file__).parent


@dataclass(frozen=True)
class Prompt:
    name: str
    text: str
    sha256: str


def load_prompt(relative_path: str) -> Prompt:
    path = PROMPT_ROOT / relative_path
    text = path.read_text(encoding="utf-8")
    return Prompt(name=relative_path, text=text, sha256=sha256(text.encode("utf-8")).hexdigest())
