"""CSS helper for Lira journey styles."""
from pathlib import Path
from typing import Optional


class LiraCSSGenerator:
    """Provide access to stored CSS assets for journey pages."""

    DEFAULT_STYLESHEET = "journey.css"

    @classmethod
    def generate(cls, filename: Optional[str] = None) -> str:
        """Return CSS content from the static directory."""
        css_path = cls._static_css_dir() / (filename or cls.DEFAULT_STYLESHEET)
        with open(css_path, "r", encoding="utf-8") as css_file:
            return css_file.read()

    @staticmethod
    def _static_css_dir() -> Path:
        return Path(__file__).resolve().parent.parent / "static" / "css"
