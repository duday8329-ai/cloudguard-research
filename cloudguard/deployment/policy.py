from __future__ import annotations

import json
from pathlib import Path


DEFAULT_POLICY = {"block_at": "HIGH", "require_clean_repair": False}


def load(path: str | None = None) -> dict:
    if not path:
        return DEFAULT_POLICY.copy()
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    policy = DEFAULT_POLICY.copy()
    policy.update(data)
    return policy
