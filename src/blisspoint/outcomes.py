"""Append-only outcome log.

Phase 1 does not score prompt shapes, it *records* them next to what happened.
The log is the raw material the eval bench will need later, so it is written
from day one even though nothing reads it yet.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

DEFAULT_LOG = Path(os.environ.get(
    "BLISSPOINT_LOG", Path.home() / ".blisspoint" / "outcomes.jsonl"))

RESULTS = ("pass", "fail", "partial", "escalated", "abandoned")


def record(brief, result: str, *, retries: int = 0, notes: str = "",
           tokens: int | None = None, path: Path | None = None) -> Path:
    if result not in RESULTS:
        raise ValueError(f"result must be one of {RESULTS}")
    path = Path(path or DEFAULT_LOG)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "target": brief.target,
        "phase": brief.phase,
        "stakes": brief.stakes,
        "dials": brief.dials.as_dict(),
        "gaps": brief.gaps,
        "brief_chars": len(brief.text),
        "result": result,
        "retries": retries,
        "tokens": tokens,
        "notes": notes,
    }
    with path.open("a") as fh:
        fh.write(json.dumps(row) + "\n")
    return path
