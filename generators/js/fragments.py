"""Load static JavaScript fragments used by the generator."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def load_runtime() -> str:
    """Return the static runtime script for journey interactions."""
    runtime_path = Path(__file__).resolve().parents[2] / "static" / "js" / "journey_runtime.js"
    return runtime_path.read_text(encoding="utf-8")
