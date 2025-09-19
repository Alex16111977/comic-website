"""Training page generator for vocabulary items."""

import random
import re
from typing import Dict, List, Optional

from .base import BaseGenerator


class TrainingPageGenerator(BaseGenerator):
    """Generate interactive training pages for vocabulary words."""

    def __init__(self, config, vocabulary_data: Optional[Dict] = None):
        super().__init__(config)
        self._data = vocabulary_data or {}
        self._words: List[Dict] = list(self._data.get("words", []))
        self._categories: Dict[str, Dict] = self._data.get("categories", {})

    def find_word(self, word_id: str) -> Optional[Dict]:
        """Return a word entry by its identifier."""
        for word in self._words:
            if word.get("id") == word_id:
                return word
        return None

    def generate_word_page(self, word: Dict) -> str:
        """Render HTML page for a given vocabulary word."""
        category_info = self._categories.get(word.get("category")) or {}
        translations = self._normalize_translation(word)
        quiz = self._build_quiz(word)
        match_game = self._build_match_game(word, category_info)
        typing_task = self._build_typing_task(word)
        related_words = self._related_words(word)

        return self.render_template(
            "trainings/word.html",
            word=word,
            category=category_info,
            translations=translations,
            quiz=quiz,
            match_game=match_game,
            typing_task=typing_task,
            related_words=related_words,
            learning_stats=self._data.get("learning_stats"),
        )

    # ------------------------------------------------------------------
    # Helpers for exercises
    # ------------------------------------------------------------------
    def _build_quiz(self, word: Dict) -> Dict:
        """Build a deterministic multiple-choice quiz for translation."""
        correct = self._extract_translation(word)
        word_label = word.get("word", "")
        article = word.get("article")

        if article:
            prompt_word = f"{article} {word_label}".strip()
        else:
            prompt_word = word_label

        question = f"Как перевести «{prompt_word}» на русский язык?"

        # Gather alternative translations for distractors
        alternatives = []
        seen = {correct}
        for other in self._words:
            if other is word:
                continue
            translation = self._extract_translation(other)
            if not translation or translation in seen:
                continue
            alternatives.append(translation)
            seen.add(translation)

        rng = random.Random(word.get("id") or prompt_word)
        rng.shuffle(alternatives)
        distractors = alternatives[:3]

        options = [
            {"label": correct, "is_correct": True}
        ]
        options.extend({"label": opt, "is_correct": False} for opt in distractors)
        rng.shuffle(options)

        return {"question": question, "options": options, "has_quiz": bool(correct)}

    def _build_match_game(self, word: Dict, category_info: Dict) -> Dict:
        """Build drag-and-drop pairs for grammatical information."""
        targets = []

        mapping = [
            ("article", "Артикль", word.get("article")),
            ("gender", "Род", word.get("gender")),
            ("plural", "Множественное число", word.get("plural")),
            ("level", "Уровень", word.get("level")),
            (
                "category",
                "Тематика",
                category_info.get("name") or word.get("category"),
            ),
            ("phonetic", "Произношение", word.get("phonetic")),
        ]

        for key, label, value in mapping:
            if value:
                targets.append({"key": key, "label": label, "value": value})

        tokens = [
            {"key": target["key"], "label": target["value"]}
            for target in targets
        ]

        rng = random.Random((word.get("id") or word.get("word")) + "-match")
        rng.shuffle(tokens)

        return {"targets": targets, "tokens": tokens, "has_game": bool(targets)}

    def _build_typing_task(self, word: Dict) -> Dict:
        """Create a short typing exercise based on the example sentence."""
        example = word.get("example") or {}
        german_sentence = None
        if isinstance(example, dict):
            german_sentence = example.get("de")
        elif isinstance(example, str):
            german_sentence = example

        base_word = word.get("word", "")
        if german_sentence and base_word:
            pattern = re.compile(re.escape(base_word), re.IGNORECASE)
            if pattern.search(german_sentence):
                prompt_sentence = pattern.sub("_____", german_sentence, count=1)
            else:
                prompt_sentence = german_sentence
        else:
            prompt_sentence = None

        hint = None
        if word.get("article"):
            hint = f"Попробуй с артиклем: {word['article']} {base_word}".strip()

        return {
            "prompt": prompt_sentence,
            "answer": base_word,
            "hint": hint,
        }

    def _related_words(self, word: Dict, limit: int = 3) -> List[Dict]:
        """Return related words from the same category."""
        category = word.get("category")
        if not category:
            return []

        related = [
            other
            for other in self._words
            if other is not word and other.get("category") == category
        ]
        related.sort(key=lambda item: item.get("id") or item.get("word", ""))

        result = []
        for entry in related[:limit]:
            translations = self._normalize_translation(entry)
            result.append(
                {
                    "id": entry.get("id"),
                    "article": entry.get("article"),
                    "word": entry.get("word"),
                    "translation_ru": translations.get("ru"),
                    "translation_en": translations.get("en"),
                }
            )
        return result

    @staticmethod
    def _extract_translation(word: Dict) -> Optional[str]:
        """Extract Russian translation if available."""
        translation = word.get("translation")
        if isinstance(translation, dict):
            return translation.get("ru") or translation.get("en")
        return translation

    @staticmethod
    def _normalize_translation(word: Dict) -> Dict[str, Optional[str]]:
        """Return RU and EN translations as a simple mapping."""
        translation = word.get("translation")
        if isinstance(translation, dict):
            return {
                "ru": translation.get("ru"),
                "en": translation.get("en"),
            }
        return {"ru": translation, "en": None}


__all__ = ["TrainingPageGenerator"]
