"""Helpers for building journey page head context."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


def _first_phase(phases: List[Dict]) -> Dict:
    return phases[0] if phases else {}


@dataclass
class HeadContext:
    """Data used to populate the hero section and progress bar."""

    initial_description: str
    first_phase_title: str
    initial_progress: int


class HeadGenerator:
    """Calculate values displayed in the page header."""

    def build(self, phases: List[Dict], progress: int) -> HeadContext:
        phase = _first_phase(phases)
        description = phase.get("description", "") if phase else ""
        title = phase.get("title", "") if phase else ""
        return HeadContext(description, title, progress)
