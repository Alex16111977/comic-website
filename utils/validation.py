"""Validation helpers for refactored modules."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Tuple


def ensure_file_length(path: Path, max_lines: int = 300) -> Tuple[bool, int]:
    """Return tuple (is_valid, line_count) for the provided file."""
    with Path(path).open("r", encoding="utf-8") as handle:
        line_count = sum(1 for _ in handle)
    return line_count <= max_lines, line_count


def ensure_directory_structure(directory: Path, required: Iterable[str]) -> List[str]:
    """Check that required files exist inside directory, return missing names."""
    missing: List[str] = []
    base = Path(directory)
    for relative in required:
        candidate = base / relative
        if not candidate.exists():
            missing.append(relative)
    return missing
