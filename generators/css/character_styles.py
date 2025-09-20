"""Character specific style composers."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

from .base_styles import BaseStyleLoader


@dataclass
class ThemeOverride:
    """Describe override rules for specific characters."""

    name: str
    rules: Dict[str, str] = field(default_factory=dict)

    def to_css(self) -> str:
        """Render override rules as CSS string."""
        lines: List[str] = []
        for selector, block in self.rules.items():
            lines.append(f"{selector} {{")
            lines.append(block)
            lines.append("}")
        return "\n".join(lines)


class CharacterStyleComposer:
    """Compose final CSS by combining base styles with overrides."""

    def __init__(
        self,
        loader: BaseStyleLoader,
        *,
        default_stylesheet: str = "journey.css",
        overrides: Optional[Iterable[ThemeOverride]] = None,
    ) -> None:
        self.loader = loader
        self.default_stylesheet = default_stylesheet
        self.overrides: List[ThemeOverride] = list(overrides or [])

    def register_override(self, override: ThemeOverride) -> None:
        """Add a new theme override."""
        self.overrides.append(override)

    def compose(self, stylesheet: Optional[str] = None) -> str:
        """Combine base stylesheet with registered overrides."""
        base_css = self.loader.load(stylesheet or self.default_stylesheet)
        override_blocks = [override.to_css() for override in self.overrides if override.rules]
        return "\n\n".join(block for block in [base_css, *override_blocks] if block)
