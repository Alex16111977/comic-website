"""Compose serialized data for journey pages."""
from __future__ import annotations

from typing import Any, Dict

from .serializer import PhaseSerializer


class JavaScriptGenerator:
    """Return the data payload required by the journey modules."""

    def generate(self, character: Dict[str, Any]) -> str:
        return PhaseSerializer(character).serialize()
