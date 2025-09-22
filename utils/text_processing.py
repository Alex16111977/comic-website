"""Text processing helpers used across generators."""
from __future__ import annotations

import re
from typing import Iterable, List

_WHITESPACE_RE = re.compile(r"\s+")
_NON_WORD_RE = re.compile(r"[^a-z0-9]+")
_SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s+")


def collapse_whitespace(value: str) -> str:
    """Collapse consecutive whitespace and trim the value."""
    return _WHITESPACE_RE.sub(" ", value or "").strip()


def slugify(value: str, *, separator: str = "-") -> str:
    """Return a URL friendly slug for the provided value."""
    value = collapse_whitespace(value).lower()
    slug = _NON_WORD_RE.sub(separator, value)
    slug = slug.strip(separator)
    return slug or "slug"


def split_sentences(text: str) -> List[str]:
    """Split text into simple sentences using punctuation heuristics."""
    text = collapse_whitespace(text)
    if not text:
        return []
    parts: Iterable[str] = _SENTENCE_END_RE.split(text)
    sentences = [segment.strip() for segment in parts if segment.strip()]
    return sentences
