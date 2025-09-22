"""JavaScript Generator for Lira Journey interactivity."""
from __future__ import annotations

from typing import Any, Dict

from .js import JavaScriptGenerator


class LiraJSGenerator:
    """Generate JavaScript bundle for journey pages."""

    @staticmethod
    def generate(character_data: Dict[str, Any]) -> str:
        return JavaScriptGenerator().generate(character_data)
