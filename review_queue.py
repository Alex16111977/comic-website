"""Utilities for managing the persistent review queue."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class QueueKey:
    """Normalized identifier for review queue entries."""

    word_id: str = ""
    character_id: str = ""
    phase_id: str = ""

    @classmethod
    def from_values(
        cls,
        word_id: Optional[str] = None,
        character_id: Optional[str] = None,
        phase_id: Optional[str] = None,
    ) -> "QueueKey":
        return cls(
            word_id=_normalize_id(word_id),
            character_id=_normalize_id(character_id),
            phase_id=_normalize_id(phase_id),
        )

    @classmethod
    def from_entry(cls, entry: Dict[str, Any]) -> "QueueKey":
        if not isinstance(entry, dict):
            return cls()
        return cls.from_values(
            entry.get("wordId") or entry.get("word_id"),
            entry.get("characterId") or entry.get("character_id"),
            entry.get("phaseId") or entry.get("phase_id"),
        )

    def matches(self, other: "QueueKey") -> bool:
        return (
            self.word_id == other.word_id
            and self.character_id == other.character_id
            and self.phase_id == other.phase_id
        )

    def as_dict(self) -> Dict[str, str]:
        return {
            "wordId": self.word_id or "",
            "characterId": self.character_id or "",
            "phaseId": self.phase_id or "",
        }


def _normalize_id(value: Optional[str]) -> str:
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value.strip()
    return str(value)


class ReviewQueueStore:
    """Persistence helper for review queue mutations."""

    def __init__(self, queue_path: Path):
        self.queue_path = Path(queue_path)

    # ------------------------------------------------------------------
    # Data access helpers
    # ------------------------------------------------------------------
    def load(self) -> List[Dict[str, Any]]:
        """Return sanitized review queue entries from disk."""
        if not self.queue_path.exists():
            return []

        try:
            with self.queue_path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return []

        if isinstance(payload, dict):
            entries = payload.get("queue", [])
        else:
            entries = payload

        if not isinstance(entries, list):
            return []

        sanitized: List[Dict[str, Any]] = []
        for raw_entry in entries:
            if not isinstance(raw_entry, dict):
                continue
            entry = dict(raw_entry)
            key = QueueKey.from_entry(entry)
            entry["wordId"] = key.word_id
            entry["characterId"] = key.character_id
            entry["phaseId"] = key.phase_id
            sanitized.append(entry)
        return sanitized

    def save(self, entries: Iterable[Dict[str, Any]]) -> None:
        """Persist queue entries to disk with a stable structure."""
        serialized = []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            normalized = dict(entry)
            key = QueueKey.from_entry(normalized)
            normalized["wordId"] = key.word_id
            normalized["characterId"] = key.character_id
            normalized["phaseId"] = key.phase_id
            serialized.append(normalized)

        self.queue_path.parent.mkdir(parents=True, exist_ok=True)
        with self.queue_path.open("w", encoding="utf-8") as handle:
            json.dump({"queue": serialized}, handle, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------
    def remove(
        self,
        word_id: Optional[str] = None,
        character_id: Optional[str] = None,
        phase_id: Optional[str] = None,
    ) -> Tuple[int, List[Dict[str, Any]]]:
        """Remove queue entries matching the provided tuple."""
        target_key = QueueKey.from_values(word_id, character_id, phase_id)
        entries = self.load()
        if not entries:
            return 0, []

        remaining: List[Dict[str, Any]] = []
        removed = 0

        for entry in entries:
            entry_key = QueueKey.from_entry(entry)
            if entry_key.matches(target_key):
                removed += 1
                continue
            remaining.append(entry)

        if removed:
            self.save(remaining)
        return removed, remaining


def remove_from_queue(
    queue_path: Path,
    word_id: Optional[str] = None,
    character_id: Optional[str] = None,
    phase_id: Optional[str] = None,
) -> int:
    """Convenience wrapper to remove entries without instantiating the store."""
    store = ReviewQueueStore(queue_path)
    removed, _ = store.remove(word_id=word_id, character_id=character_id, phase_id=phase_id)
    return removed
