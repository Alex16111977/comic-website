"""Index page generator with character cards"""
import json
import re

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
        queue_items = self._load_review_queue()
        if not queue_items:
            return []

        vocabulary_words = self._load_vocabulary_words()
        if not vocabulary_words:
            return []

        word_index = {
            word.get("id"): word
            for word in vocabulary_words
            if isinstance(word, dict) and word.get("id")
        }

        slug_index = {}
        for word in vocabulary_words:
            if not isinstance(word, dict):
                continue
            for slug in self._slugs_for_vocabulary(word):
                slug_index.setdefault(slug, word)

        review_items = []
        character_cache = {}

        for entry in queue_items:
            if limit and len(review_items) >= limit:
                break

            if not isinstance(entry, dict):
                continue

            word_entry = None
            candidate_ids = [
                entry.get("vocabulary_id"),
                entry.get("word_id"),
                entry.get("id"),
            ]

            for candidate in candidate_ids:
                if candidate and candidate in word_index:
                    word_entry = word_index[candidate]
                    break

            if not word_entry:
                slug_candidates = [
                    entry.get("word_slug"),
                    entry.get("slug"),
                    self._slugify_text(entry.get("word")),
                ]
                for slug in slug_candidates:
                    if slug and slug in slug_index:
                        word_entry = slug_index[slug]
                        break

            if not word_entry:
                continue

            word_id = word_entry.get("id") or self._get_item_id(word_entry)
            character_id = entry.get("character_id")
            phase_id = entry.get("phase_id")
            character_meta = self._get_character_meta(character_id, character_cache)
            phase_meta = {}
            if character_meta:
                phase_meta = (character_meta.get("phases") or {}).get(phase_id, {})

            review_items.append(
                {
                    "id": word_id,
                    "emoji": entry.get("emoji") or word_entry.get("emoji", "📝"),
                    "word": self._format_word(word_entry),
                    "translation": self._extract_translation(word_entry),
                    "level": word_entry.get("level"),
                    "category": word_entry.get("category"),
                    "phonetic": word_entry.get("phonetic"),
                    "example": self._extract_example(word_entry),
                    "practice_url": f"trainings/{word_id}.html",
                    "word_slug": self._slugify_text(word_entry.get("word")) or entry.get("word_slug"),
                    "character_id": character_id,
                    "character_name": character_meta.get("name") if character_meta else None,
                    "character_title": character_meta.get("title") if character_meta else None,
                    "phase_id": phase_id,
                    "phase_title": phase_meta.get("title") if phase_meta else None,
                    "added_at": entry.get("added_at"),
                }
            )

        return review_items

    def _load_review_queue(self):
        """Load queued vocabulary selections from JSON storage."""
        queue_path = self.config.DATA_DIR / "review_queue.json"
        if not queue_path.exists():
            return []

        try:
            with queue_path.open("r", encoding="utf-8") as fp:
                queue_data = json.load(fp)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[WARNING] Unable to load review queue: {exc}")
            return []

        items = queue_data.get("items")
        if not isinstance(items, list):
            return []

        enumerated = [
            (index, item)
            for index, item in enumerate(items)
            if isinstance(item, dict)
        ]

        enumerated.sort(
            key=lambda pair: (
                self._priority_value(pair[1].get("priority")),
                pair[1].get("added_at") or "",
                pair[0],
            )
        )

        return [item for _, item in enumerated]

    def _load_vocabulary_words(self):
        """Load detailed vocabulary data."""
        vocabulary_path = self.config.DATA_DIR / "vocabulary" / "words.json"
        if not vocabulary_path.exists():
            return []

        try:
            with vocabulary_path.open("r", encoding="utf-8") as fp:
                vocabulary = json.load(fp)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[WARNING] Unable to load vocabulary data: {exc}")
            return []

        words = vocabulary.get("words")
        if not isinstance(words, list):
            return []
        return words

    def _get_character_meta(self, character_id, cache):
        """Return character metadata with phase titles."""
        if not character_id:
            return {}

        if character_id in cache:
            return cache[character_id]

        char_file = self.config.CHARACTERS_DIR / f"{character_id}.json"
        if not char_file.exists():
            cache[character_id] = {}
            return cache[character_id]

        try:
            data = self.load_character(char_file)
        except (OSError, json.JSONDecodeError):
            cache[character_id] = {}
            return cache[character_id]

        phases = {}
        for phase in data.get("journey_phases", []):
            if not isinstance(phase, dict):
                continue
            phase_id = phase.get("id")
            if not phase_id:
                continue
            phases[phase_id] = {
                "title": phase.get("title"),
                "icon": phase.get("icon"),
            }

        cache[character_id] = {
            "id": character_id,
            "name": data.get("name"),
            "title": data.get("title"),
            "phases": phases,
        }
        return cache[character_id]

    def _slugs_for_vocabulary(self, word):
        """Return possible slug representations for vocabulary entry."""
        slugs = set()
        if not isinstance(word, dict):
            return slugs

        base = word.get("word")
        article = word.get("article")

        slug_candidates = [
            base,
            f"{article} {base}" if article and base else None,
        ]

        for value in slug_candidates:
            slug = self._slugify_text(value)
            if slug:
                slugs.add(slug)

        return slugs

    @staticmethod
    def _slugify_text(value):
        """Normalize a string into a slug."""
        if not value:
            return None
        slug = re.sub(r"[^a-z0-9]+", "-", str(value).lower())
        slug = slug.strip("-")
        return slug or None

    @staticmethod
    def _priority_value(value):
        """Convert optional priority into sortable integer."""
        try:
            return int(value)
        except (TypeError, ValueError):
            return 9999

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
