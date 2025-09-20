"""Utilities to work with CSS animations."""
from __future__ import annotations

import re
from typing import Dict, Iterable, Optional

_KEYFRAME_RE = re.compile(r"@keyframes\s+([\w-]+)\s*\{(.*?)\}", re.DOTALL)


class AnimationExtractor:
    """Extract keyframe definitions from CSS blocks."""

    def extract(self, css: str) -> Dict[str, str]:
        """Return mapping of animation name to body."""
        matches = _KEYFRAME_RE.findall(css or "")
        return {name: body.strip() for name, body in matches}

    def isolate(self, css: str, names: Optional[Iterable[str]] = None) -> str:
        """Return CSS containing only the requested animations."""
        animations = self.extract(css)
        if names is not None:
            animations = {name: animations[name] for name in names if name in animations}
        blocks = [f"@keyframes {name} {{{body}}}" for name, body in animations.items()]
        return "\n\n".join(blocks)
