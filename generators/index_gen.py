"""Index page generator with character cards"""
import json

from .base import BaseGenerator


class IndexGenerator(BaseGenerator):
    """Generate index page with all character journeys"""

    def generate(self, character_files, review_items=None):
        """Generate index page with character grid"""
        role_descriptions = {
            "king_lear": "Трагический король",
            "cordelia": "Верная дочь",
            "goneril": "Старшая дочь-предательница",
            "regan": "Младшая дочь-предательница",
            "gloucester": "Благородный граф",
            "edgar": "Законный сын Глостера",
            "edmund": "Бастард Глостера",
            "kent": "Верный советник",
            "fool": "Мудрый шут",
            "albany": "Муж Гонерильи",
            "cornwall": "Муж Реганы",
            "oswald": "Управляющий Гонерильи",
        }

        cards = []
        phase_total = 0
        vocabulary_total = 0

        for char_file in character_files:
            character = self.load_character(char_file)
            char_id = char_file.stem
            journey_phases = character.get("journey_phases", [])

            phase_total += len(journey_phases)
            vocabulary_total += sum(len(phase.get("vocabulary", [])) for phase in journey_phases)

            first_icon = journey_phases[0]["icon"] if journey_phases else "👤"
            role = role_descriptions.get(char_id, character.get("title", "Персонаж"))

            cards.append(
                {
                    "id": char_id,
                    "icon": first_icon,
                    "name": character["name"],
                    "role": role,
                    "phase_count": len(journey_phases),
                    "url": f"journeys/{char_file.stem}.html",
                }
            )

        if review_items is None:
            review_items = self.get_review_items()

        return self.render_template(
            "index.html",
            cards=cards,
            character_count=len(cards),
            phase_total=phase_total,
            vocabulary_total=vocabulary_total,
            review_items=review_items,
        )

    def get_review_items(self, limit=6):
        """Public helper to provide review items for other generators."""
        return self._get_review_items(limit=limit)

    def _get_review_items(self, limit=6):
        """Return a curated list of vocabulary items for spaced repetition."""
        vocabulary_path = self.config.DATA_DIR / "vocabulary" / "words.json"
        if not vocabulary_path.exists():
            return []

        try:
            with open(vocabulary_path, "r", encoding="utf-8") as f:
                vocabulary = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[WARNING] Unable to load vocabulary data: {exc}")
            return []

        words = vocabulary.get("words", [])
        if not isinstance(words, list):
            return []

        pending_words = [word for word in words if not word.get("learned", False)]
        if not pending_words:
            pending_words = words

        sorted_words = sorted(pending_words, key=self._review_sort_key)
        selected_words = sorted_words[:limit]

        review_items = []
        for word in selected_words:
            review_items.append(
                {
                    "id": self._get_item_id(word),
                    "emoji": word.get("emoji", "📝"),
                    "word": self._format_word(word),
                    "translation": self._extract_translation(word),
                    "level": word.get("level"),
                    "category": word.get("category"),
                    "phonetic": word.get("phonetic"),
                    "example": self._extract_example(word),
                    "practice_url": f"trainings/{self._get_item_id(word)}.html",
                }
            )

        return review_items

    def _review_sort_key(self, word):
        """Sort vocabulary by frequency, level and alphabetical order."""
        frequency_order = {"high": 0, "medium": 1, "low": 2}
        frequency = word.get("frequency")
        frequency_rank = 3
        if isinstance(frequency, str):
            frequency_rank = frequency_order.get(frequency.lower(), 3)

        level = word.get("level") or "Z"
        word_value = word.get("word") or ""

        return (frequency_rank, level, word_value)

    def _get_item_id(self, word):
        """Return stable identifier for vocabulary item."""
        return word.get("id") or (word.get("word") or "vocab").replace(" ", "_")

    def _format_word(self, word):
        """Compose article and base word for display."""
        base = word.get("word", "")
        article = word.get("article")
        if article:
            return f"{article} {base}".strip()
        return base

    def _extract_translation(self, word):
        """Extract Russian translation (fallback to English/string)."""
        translation = word.get("translation")
        if isinstance(translation, dict):
            return translation.get("ru") or translation.get("en")
        return translation

    def _extract_example(self, word):
        """Return German example sentence if available."""
        example = word.get("example")
        if isinstance(example, dict):
            return example.get("de")
        return example
