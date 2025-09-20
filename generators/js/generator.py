"""Compose the final JavaScript bundle."""
from __future__ import annotations

from typing import Any, Dict

from .fragments import load_runtime
from .serializer import PhaseSerializer


class JavaScriptGenerator:
    """Combine serialized data with the runtime script."""

    def __init__(self, runtime_loader=load_runtime) -> None:
        self.runtime_loader = runtime_loader

    def generate(self, character: Dict[str, Any]) -> str:
        header = PhaseSerializer(character).serialize()
        runtime = self.runtime_loader()
        return f"{header}{runtime}"
