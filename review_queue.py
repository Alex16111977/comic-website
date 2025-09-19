"""Review queue persistence helpers for King Lear Comic Generator."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class QueueKey:
    """Represents a unique key for a review queue item."""
    
    def __init__(self, word_id: str, character_id: str = "", phase_id: str = ""):
        self.word_id = self._normalize(word_id)
        self.character_id = self._normalize(character_id)
        self.phase_id = self._normalize(phase_id)
    
    @staticmethod
    def _normalize(value: Optional[str]) -> str:
        """Normalize ID values by stripping whitespace and handling None."""
        if value is None:
            return ""
        return value.strip()
    
    @classmethod
    def from_entry(cls, entry: Dict[str, Any]) -> 'QueueKey':
        """Create a QueueKey from a queue entry dictionary."""
        return cls(
            word_id=entry.get("wordId", ""),
            character_id=entry.get("characterId", ""),
            phase_id=entry.get("phaseId", "")
        )
    
    def matches(self, word_id: str, character_id: str = "", phase_id: str = "") -> bool:
        """Check if this key matches the given parameters."""
        return (
            self.word_id == self._normalize(word_id) and
            self.character_id == self._normalize(character_id) and
            self.phase_id == self._normalize(phase_id)
        )
    
    def to_entry(self) -> Dict[str, str]:
        """Convert to dictionary entry format."""
        return {
            "wordId": self.word_id,
            "characterId": self.character_id,
            "phaseId": self.phase_id
        }


class ReviewQueueStore:
    """Handles persistence of review queue items to JSON file."""
    
    def __init__(self, queue_path: Path | str):
        """Initialize store with path to queue JSON file."""
        self.queue_path = Path(queue_path)
    
    def load(self) -> List[Dict[str, Any]]:
        """Load queue items from file. Returns empty list if file doesn't exist."""
        if not self.queue_path.exists():
            return []
        
        try:
            with self.queue_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("queue", [])
        except (json.JSONDecodeError, IOError):
            return []
    
    def save(self, queue_items: List[Dict[str, Any]]) -> None:
        """Save queue items to file."""
        data = {"queue": queue_items}
        
        # Ensure parent directory exists
        self.queue_path.parent.mkdir(parents=True, exist_ok=True)
        
        with self.queue_path.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add(self, word_id: str, character_id: str = "", phase_id: str = "") -> None:
        """Add a new item to the queue."""
        queue_items = self.load()
        
        # Check if item already exists
        key = QueueKey(word_id, character_id, phase_id)
        for item in queue_items:
            if QueueKey.from_entry(item).matches(word_id, character_id, phase_id):
                return  # Item already exists
        
        # Add new item
        queue_items.append(key.to_entry())
        self.save(queue_items)
    
    def remove(self, word_id: str, character_id: str = "", phase_id: str = "") -> Tuple[int, List[Dict[str, Any]]]:
        """
        Remove matching items from the queue.
        
        Returns:
            Tuple of (number of removed items, remaining items list)
        """
        queue_items = self.load()
        remaining = []
        removed_count = 0
        
        for item in queue_items:
            key = QueueKey.from_entry(item)
            if key.matches(word_id, character_id, phase_id):
                removed_count += 1
            else:
                remaining.append(item)
        
        # Save updated queue if items were removed
        if removed_count > 0:
            self.save(remaining)
        
        return removed_count, remaining
    
    def clear(self) -> None:
        """Clear all items from the queue."""
        self.save([])
    
    def count(self) -> int:
        """Get the number of items in the queue."""
        return len(self.load())
