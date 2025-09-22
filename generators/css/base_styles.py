"""Base helpers for loading CSS assets."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional


@dataclass
class BaseStyleLoader:
    """Provide access to CSS files stored on disk."""

    css_directory: Optional[Path] = None

    def __post_init__(self) -> None:
        if self.css_directory is None:
            self.css_directory = Path(__file__).resolve().parents[2] / "static" / "css"
        else:
            self.css_directory = Path(self.css_directory)

    def stylesheet_path(self, name: str) -> Path:
        """Return absolute path to a stylesheet."""
        return self.css_directory / name

    def load(self, name: str) -> str:
        """Read CSS content from disk."""
        path = self.stylesheet_path(name)
        with path.open("r", encoding="utf-8") as handle:
            return handle.read()

    def available_stylesheets(self) -> List[str]:
        """Return list of available CSS filenames."""
        if not self.css_directory.exists():
            return []
        return [item.name for item in self.css_directory.iterdir() if item.suffix == ".css"]

    def load_many(self, names: Iterable[str]) -> str:
        """Join multiple stylesheets into a single string."""
        contents = [self.load(name) for name in names]
        return "\n\n".join(filter(None, contents))
