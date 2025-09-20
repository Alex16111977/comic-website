"""CSS helper for Lira journey styles."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Optional

from .css import AnimationExtractor, BaseStyleLoader, CharacterStyleComposer, ThemeOverride


class LiraCSSGenerator:
    """Provide access to stored CSS assets for journey pages."""

    DEFAULT_STYLESHEET = "journey.css"

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]
        self._loader = BaseStyleLoader(self.base_dir / "static" / "css")
        self._composer = CharacterStyleComposer(
            self._loader, default_stylesheet=self.DEFAULT_STYLESHEET
        )
        self._animation_extractor = AnimationExtractor()

    def register_theme(self, name: str, rules: Dict[str, str]) -> None:
        """Register per-character override rules."""
        self._composer.register_override(ThemeOverride(name=name, rules=rules))

    def generate(self, filename: Optional[str] = None) -> str:
        """Return CSS content composed from base styles and overrides."""
        return self._composer.compose(filename)

    def extract_animations(
        self, css: Optional[str] = None, names: Optional[Iterable[str]] = None
    ) -> str:
        """Return animation definitions for the provided CSS fragment."""
        css_source = css if css is not None else self.generate()
        return self._animation_extractor.isolate(css_source, names)

    @property
    def css_directory(self) -> Path:
        """Expose directory that stores CSS assets."""
        return self._loader.css_directory
