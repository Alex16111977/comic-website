"""Serialize character journeys into JavaScript-friendly payloads."""
from __future__ import annotations

import json
from typing import Any, Dict, List


def _ensure_list(value: Any) -> List[Any]:
    if not value:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple):
        return [item for item in value]
    return [value]


class PhaseSerializer:
    """Transform character data into JS declarations."""

    def __init__(self, character: Dict[str, Any]) -> None:
        self.character = character

    def serialize(self) -> str:
        phase_map = self._build_phase_map()
        character_id = self.character.get("id") or self.character.get("slug") or "journey"
        parts = [
            "const phaseVocabularies = ",
            f"{json.dumps(phase_map, ensure_ascii=False, indent=4)};\n\n",
            f"const characterId = {json.dumps(character_id)};\n",
            "const STORAGE_PREFIX = 'liraJourney';\n",
            "const REVIEW_QUEUE_KEY = `${STORAGE_PREFIX}:reviewQueue`;\n",
            "const quizStateCache = {};\n\n",
            "window.phaseData = phaseVocabularies;\n",
            "window.phaseKeys = Object.keys(phaseVocabularies);\n\n",
        ]
        return "".join(parts)

    def _build_phase_map(self) -> Dict[str, Any]:
        phases: Dict[str, Any] = {}
        for phase in self.character.get("journey_phases", []):
            phase_id = phase.get("id")
            if not phase_id:
                continue
            vocabulary_entries = [self._serialize_vocabulary_entry(word) for word in phase.get("vocabulary", [])]
            phases[phase_id] = {
                "title": phase.get("title", ""),
                "description": phase.get("description", ""),
                "vocabulary": vocabulary_entries,
                "words": [self._serialize_word(word) for word in phase.get("vocabulary", [])],
                "quizzes": [self._serialize_quiz(quiz) for quiz in phase.get("quizzes", [])],
                "quizAttempts": {},
                "sentenceParts": self._sentence_constructors(phase),
            }
        return phases

    @staticmethod
    def _serialize_vocabulary_entry(word: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "german": word.get("german", ""),
            "russian": word.get("russian", ""),
            "sentence": word.get("sentence", ""),
            "sentence_translation": word.get("sentence_translation", ""),
            "russian_hint": word.get("russian_hint", ""),
            "transcription": word.get("transcription", ""),
            "themes": _ensure_list(word.get("themes")),
            "sentence_parts": _ensure_list(word.get("sentence_parts")),
            "synonyms": _ensure_list(word.get("synonyms")),
            "visual_hint": word.get("visual_hint", ""),
        }

    @staticmethod
    def _serialize_word(word: Dict[str, Any]) -> Dict[str, Any]:
        themes = _ensure_list(word.get("themes"))
        word_family = _ensure_list(word.get("wordFamily"))
        collocations = _ensure_list(word.get("collocations"))
        sentence_parts = _ensure_list(word.get("sentence_parts"))
        return {
            "word": word.get("german", ""),
            "translation": word.get("russian", ""),
            "russian_hint": word.get("russian_hint", ""),
            "transcription": word.get("transcription", ""),
            "sentence": word.get("sentence", ""),
            "sentenceTranslation": word.get("sentence_translation", ""),
            "visual_hint": word.get("visual_hint", ""),
            "themes": themes,
            "wordFamily": word_family,
            "collocations": collocations,
            "sentenceParts": sentence_parts,
        }

    @staticmethod
    def _serialize_quiz(quiz: Dict[str, Any]) -> Dict[str, Any]:
        choices = list(quiz.get("choices", []))
        correct_index = quiz.get("correct_index", quiz.get("correctIndex", 0))
        try:
            correct_index = int(correct_index)
        except (TypeError, ValueError):
            correct_index = 0
        return {
            "question": quiz.get("question", ""),
            "choices": choices,
            "correctIndex": correct_index,
        }

    @staticmethod
    def _sentence_constructors(phase: Dict[str, Any]) -> List[Dict[str, Any]]:
        constructors: List[Dict[str, Any]] = []
        for vocab in phase.get("vocabulary", []):
            parts = _ensure_list(vocab.get("sentence_parts"))
            if len(parts) > 1:
                constructors.append(
                    {
                        "word": vocab.get("german", ""),
                        "translation": vocab.get("russian", ""),
                        "parts": parts,
                        "sentence": vocab.get("sentence", ""),
                        "sentenceTranslation": vocab.get("sentence_translation", ""),
                    }
                )
        return constructors
