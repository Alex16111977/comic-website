"""Tests for review queue persistence helpers."""
from __future__ import annotations

import json
from pathlib import Path

from review_queue import QueueKey, ReviewQueueStore


def build_queue_file(tmp_path: Path, entries):
    queue_path = tmp_path / "review_queue.json"
    queue_path.write_text(json.dumps({"queue": entries}, ensure_ascii=False, indent=2), encoding="utf-8")
    return queue_path


def test_remove_matching_tuple(tmp_path):
    entries = [
        {"wordId": "w1", "characterId": "char", "phaseId": "phase"},
        {"wordId": "w2", "characterId": "char", "phaseId": "phase"},
    ]
    queue_path = build_queue_file(tmp_path, entries)
    store = ReviewQueueStore(queue_path)

    removed, remaining = store.remove("w1", "char", "phase")

    assert removed == 1
    assert len(remaining) == 1
    assert remaining[0]["wordId"] == "w2"
    assert queue_path.exists()

    saved = json.loads(queue_path.read_text(encoding="utf-8"))
    assert len(saved["queue"]) == 1
    assert saved["queue"][0]["wordId"] == "w2"


def test_remove_normalizes_ids(tmp_path):
    entries = [
        {"wordId": "  w3  ", "characterId": "  ", "phaseId": None},
        {"wordId": "w4", "characterId": "c4", "phaseId": "p4"},
    ]
    queue_path = build_queue_file(tmp_path, entries)
    store = ReviewQueueStore(queue_path)

    removed, remaining = store.remove("w3", "", "")

    assert removed == 1
    assert all(QueueKey.from_entry(entry).word_id != "w3" for entry in remaining)


def test_load_returns_empty_for_missing_file(tmp_path):
    queue_path = tmp_path / "missing.json"
    store = ReviewQueueStore(queue_path)

    assert store.load() == []

    removed, remaining = store.remove("w1", "", "")
    assert removed == 0
    assert remaining == []
