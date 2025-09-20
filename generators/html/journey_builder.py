"""Build journey phase data, exercises and quizzes."""
from __future__ import annotations
import json
import random
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from .vocabulary_processor import VocabularyProcessor


@dataclass
class JourneyAssets:
    phases: List[Dict[str, Any]]
    exercises: List[Dict[str, Any]]
    quizzes: List[Dict[str, Any]]
    quizzes_json: str
    relations_metadata: Dict[str, Dict[str, bool]]

class JourneyBuilder:
    """Construct interactive data for a character journey."""

    def __init__(self, vocabulary: VocabularyProcessor) -> None:
        self.vocabulary = vocabulary

    def prepare(self, character: Dict[str, Any]) -> JourneyAssets:
        phases = list(character.get("journey_phases", []))
        self._ensure_phase_ids(phases)
        exercises, quizzes, quizzes_json = self._prepare_interactions(phases)
        metadata = self.vocabulary.relations_metadata(phases)
        return JourneyAssets(phases, exercises, quizzes, quizzes_json, metadata)

    @staticmethod
    def initial_progress(phases: List[Any]) -> int:
        count = len(phases)
        return 0 if count == 0 else max(1, int(100 / count))

    @staticmethod
    def _ensure_phase_ids(phases: List[Dict[str, Any]]) -> None:
        for index, phase in enumerate(phases):
            phase.setdefault("id", f"phase-{index}")

    def _prepare_interactions(self, phases: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], str]:
        exercises: List[Dict[str, Any]] = []
        quizzes: List[Dict[str, Any]] = []
        quizzes_map: Dict[str, List[Dict[str, Any]]] = {}
        for index, phase in enumerate(phases):
            phase_id = phase.get("id", f"phase-{index}")
            vocab_words, constructor_entries = self._collect_vocabulary(phase)
            phase["sentence_parts"] = constructor_entries
            phase_quizzes = self._build_phase_quizzes(phase, vocab_words)
            phase["quizzes"] = phase_quizzes
            quizzes.append({"phase_id": phase_id, "questions": phase_quizzes, "is_active": index == 0})
            quizzes_map[phase_id] = phase_quizzes
            exercise = self._build_exercise(index, phase, phase_id)
            if exercise:
                exercises.append(exercise)
        return exercises, quizzes, json.dumps(quizzes_map, ensure_ascii=False)

    @staticmethod
    def _collect_vocabulary(phase: Dict[str, Any]) -> Tuple[List[Tuple[str, str]], List[Dict[str, Any]]]:
        entries = phase.get("vocabulary", [])
        vocab_words = []
        constructor_entries: List[Dict[str, Any]] = []
        for entry in entries:
            german = (entry.get("german") or "").strip()
            russian = (entry.get("russian") or "").strip()
            if german and russian:
                vocab_words.append((german, russian))
            parts = entry.get("sentence_parts")
            if isinstance(parts, list) and len(parts) > 1:
                constructor_entries.append(
                    {
                        "german": german,
                        "russian": russian,
                        "sentence": entry.get("sentence", ""),
                        "sentence_translation": entry.get("sentence_translation", ""),
                        "parts": parts,
                    }
                )
        return vocab_words, constructor_entries

    def _build_phase_quizzes(self, phase: Dict[str, Any], vocabulary_words: List[Tuple[str, str]]) -> List[Dict[str, Any]]:
        existing = list(phase.get("quizzes", []))
        referenced = {
            word.lower()
            for word in (self._extract_question_word(quiz.get("question")) for quiz in existing)
            if word
        }
        if vocabulary_words:
            translations = [russian for _, russian in vocabulary_words]
            for german, russian in vocabulary_words:
                if german.lower() in referenced:
                    continue
                distractors = [t for t in translations if t.lower() != russian.lower()]
                if len(distractors) > 3:
                    distractors = random.sample(distractors, 3)
                new_quiz = {
                    "question": f"Что означает немецкое слово «{german}»?",
                    "choices": [russian, *distractors],
                    "correct_index": 0,
                }
                existing.append(new_quiz)
                referenced.add(german.lower())
        phase_quizzes: List[Dict[str, Any]] = []
        for quiz in existing:
            choices = list(quiz.get("choices", []))
            correct_index = quiz.get("correct_index", quiz.get("correctIndex", 0))
            correct_choice = choices[correct_index] if 0 <= correct_index < len(choices) else None
            random.shuffle(choices)
            correct_index = choices.index(correct_choice) if correct_choice in choices else (0 if choices else 0)
            phase_quizzes.append({"question": quiz.get("question", ""), "choices": choices, "correct_index": correct_index})
        return phase_quizzes

    @staticmethod
    def _extract_question_word(question: Any) -> Optional[str]:
        if not question:
            return None
        match = re.search(r"«([^»]+)»", question)
        if match:
            return match.group(1).strip()
        match = re.search(r'"([^"]+)"', question)
        if match:
            return match.group(1).strip()
        return None

    def _build_exercise(self, index: int, phase: Dict[str, Any], phase_id: str) -> Optional[Dict[str, Any]]:
        scene = phase.get("theatrical_scene")
        if not scene or not scene.get("exercise_text"):
            return None
        words_dict = self.vocabulary.words_dictionary(phase, scene)
        rendered = re.sub(
            r'___ \(([^)]+)\)',
            lambda match: self._replace_blank(match, words_dict),
            scene["exercise_text"],
        )
        return {
            "phase_id": phase_id,
            "title": scene.get("title", ""),
            "text": rendered,
            "is_active": index == 0,
        }

    @staticmethod
    def _replace_blank(match: re.Match, words_dict: Dict[str, str]) -> str:
        hint = match.group(1)
        answer = words_dict.get(hint, "UNKNOWN")
        return (
            f'<span class="blank" data-answer="{answer}" '
            f'data-hint="{hint}">_______ ({hint})</span>'
        )
