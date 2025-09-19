"""HTML Generator for Lira Journey pages"""
import json
import random
import re
from pathlib import Path

from .base import BaseGenerator
from .js_lira import LiraJSGenerator


class LiraHTMLGenerator(BaseGenerator):
    """Generate complete HTML pages in lira-journey style"""

    _vocabulary_cache = None

    @classmethod
    def _load_vocabulary_cache(cls):
        """Load vocabulary enrichment data once."""
        if cls._vocabulary_cache is not None:
            return cls._vocabulary_cache

        vocab_path = (
            Path(__file__).resolve().parents[1]
            / 'data'
            / 'vocabulary'
            / 'vocabulary.json'
        )

        cache = {}
        if vocab_path.exists():
            with vocab_path.open('r', encoding='utf-8') as fp:
                data = json.load(fp)
            for entry in data.get('vocabulary', []):
                german = (entry.get('german') or '').strip().lower()
                if german:
                    cache[german] = entry

        cls._vocabulary_cache = cache
        return cls._vocabulary_cache

    @classmethod
    def _enrich_character_vocabulary(cls, character):
        """Attach word relations from shared vocabulary to character words."""
        vocab_index = cls._load_vocabulary_cache()
        if not vocab_index:
            return

        for phase in character.get('journey_phases', []):
            for word in phase.get('vocabulary', []):
                german = (word.get('german') or '').strip().lower()
                if not german:
                    continue
                entry = vocab_index.get(german)
                if not entry:
                    continue

                if 'wordFamily' not in word or not word['wordFamily']:
                    word['wordFamily'] = list(entry.get('word_family', []))
                if 'synonyms' not in word or not word['synonyms']:
                    word['synonyms'] = list(entry.get('synonyms', []))
                if 'collocations' not in word or not word['collocations']:
                    word['collocations'] = list(entry.get('collocations', []))

    def generate_journey(self, character_file):
        """Generate journey page for a character"""
        character = self.load_character(character_file)
        self._enrich_character_vocabulary(character)
        journey_phases = character.get("journey_phases", [])

        for index, phase in enumerate(journey_phases):
            if not phase.get("id"):
                phase["id"] = f"phase-{index}"

        exercises, quizzes, quizzes_json = self._prepare_exercises(journey_phases)

        relations_metadata = self._collect_relations_metadata(journey_phases)
        js = LiraJSGenerator.generate(character)
        initial_description = journey_phases[0].get("description", "") if journey_phases else ""
        first_phase_title = journey_phases[0].get("title", "") if journey_phases else ""
        initial_progress = self._initial_progress_percentage(len(journey_phases))

        return self.render_template(
            "journey.html",
            character=character,
            journey_phases=journey_phases,
            exercises=exercises,
            quizzes=quizzes,
            quizzes_json=quizzes_json,
            initial_description=initial_description,
            initial_progress=initial_progress,
            first_phase_title=first_phase_title,
            relations_metadata=relations_metadata,
            js=js,
        )

    def _collect_relations_metadata(self, journey_phases):
        """Build metadata to control visibility of relation sections."""
        metadata = {}

        for index, phase in enumerate(journey_phases):
            phase_id = phase.get("id", f"phase-{index}")

            has_word_families = False
            has_synonyms = False
            has_collocations = False

            for word in phase.get("vocabulary", []):
                word_family = word.get("wordFamily")
                if isinstance(word_family, str):
                    word_family = [word_family]
                elif not isinstance(word_family, list):
                    word_family = []
                if word_family:
                    has_word_families = True

                synonyms = word.get("synonyms")
                if isinstance(synonyms, str):
                    synonyms = [synonyms]
                elif not isinstance(synonyms, list):
                    synonyms = []
                if synonyms:
                    has_synonyms = True

                collocations = word.get("collocations")
                if isinstance(collocations, str):
                    collocations = [collocations]
                elif not isinstance(collocations, list):
                    collocations = []
                if collocations:
                    has_collocations = True

            metadata[phase_id] = {
                "has_word_families": has_word_families,
                "has_synonyms": has_synonyms,
                "has_collocations": has_collocations,
                "has_relations": has_word_families or has_synonyms or has_collocations,
            }

        return metadata

    def _prepare_exercises(self, journey_phases):
        """Prepare exercises with blanks replaced by interactive spans."""
        exercises = []
        quizzes = []
        quizzes_map = {}

        def _extract_question_word(question):
            """Try to pull the german lexeme referenced in a quiz question."""
            if not question:
                return None

            match = re.search(r"«([^»]+)»", question)
            if match:
                return match.group(1).strip()

            match = re.search(r'"([^"]+)"', question)
            if match:
                return match.group(1).strip()

            return None

        for index, phase in enumerate(journey_phases):
            phase_id = phase.get("id", f"phase-{index}")
            scene = phase.get("theatrical_scene")

            vocabulary_words = []
            for entry in phase.get("vocabulary", []):
                german = (entry.get("german") or "").strip()
                russian = (entry.get("russian") or "").strip()
                if german and russian:
                    vocabulary_words.append((german, russian))

            existing_quizzes_data = list(phase.get("quizzes", []))
            referenced_words = {
                word.lower()
                for word in (
                    _extract_question_word(quiz.get("question"))
                    for quiz in existing_quizzes_data
                )
                if word
            }

            if vocabulary_words:
                all_translations = [russian for _, russian in vocabulary_words]
                for german, russian in vocabulary_words:
                    if german.lower() in referenced_words:
                        continue

                    distractor_pool = [
                        option
                        for option in all_translations
                        if option.lower() != russian.lower()
                    ]

                    distractor_count = min(3, len(distractor_pool))
                    if distractor_count < 2:
                        distractor_count = len(distractor_pool)

                    if distractor_count:
                        distractors = random.sample(distractor_pool, distractor_count)
                    else:
                        distractors = []

                    new_quiz = {
                        "question": f"Что означает немецкое слово «{german}»?",
                        "choices": [russian, *distractors],
                        "correct_index": 0,
                    }
                    existing_quizzes_data.append(new_quiz)
                    referenced_words.add(german.lower())

            phase_quizzes = []
            for quiz in existing_quizzes_data:
                choices = list(quiz.get("choices", []))
                correct_index = quiz.get("correct_index", 0)

                correct_choice = None
                if 0 <= correct_index < len(choices):
                    correct_choice = choices[correct_index]

                random.shuffle(choices)

                if correct_choice is not None and choices:
                    try:
                        correct_index = choices.index(correct_choice)
                    except ValueError:
                        correct_index = 0
                else:
                    correct_index = 0

                phase_quizzes.append(
                    {
                        "question": quiz.get("question", ""),
                        "choices": choices,
                        "correct_index": correct_index,
                    }
                )

            phase["quizzes"] = phase_quizzes

            quizzes.append(
                {
                    "phase_id": phase_id,
                    "questions": phase_quizzes,
                    "is_active": index == 0,
                }
            )
            quizzes_map[phase_id] = phase_quizzes

            if not scene:
                continue

            exercise_text = scene.get("exercise_text")
            if not exercise_text:
                continue

            words_dict = self._build_words_dictionary(phase, scene)

            def replace_blank(match):
                hint = match.group(1)
                answer = words_dict.get(hint, "UNKNOWN")
                return (
                    f'<span class="blank" data-answer="{answer}" '
                    f'data-hint="{hint}">_______ ({hint})</span>'
                )

            rendered_text = re.sub(r'___ \(([^)]+)\)', replace_blank, exercise_text)

            exercises.append(
                {
                    "phase_id": phase_id,
                    "title": scene["title"],
                    "text": rendered_text,
                    "is_active": index == 0,
                }
            )

        quizzes_json = json.dumps(quizzes_map, ensure_ascii=False)

        return exercises, quizzes, quizzes_json

    def _build_words_dictionary(self, phase, scene):
        """Build dictionary with vocabulary answers for blanks."""
        words_dict = {}

        for vocab in phase.get("vocabulary", []):
            german = vocab["german"]
            russian = vocab["russian"]

            if german.startswith(("der ", "die ", "das ")):
                parts = german.split(" ", 1)
                words_dict[russian] = f"{parts[0]} {parts[1].upper()}"
            else:
                words_dict[russian] = german.upper()

            if russian == "трон":
                words_dict["троне"] = words_dict[russian]
            elif russian == "церемония":
                words_dict["церемонию"] = words_dict[russian]
            elif russian == "гнев":
                words_dict["гнев"] = words_dict[russian]
            elif russian == "проклятие":
                words_dict["проклятием"] = words_dict[russian]
            elif russian == "нищета":
                words_dict["нищету"] = words_dict[russian]
            elif russian == "хижина":
                words_dict["хижине"] = words_dict[russian]
            elif russian == "правда":
                words_dict["правду"] = words_dict[russian]
            elif russian == "конец":
                words_dict["концом"] = words_dict[russian]
            elif russian == "слеза":
                words_dict["слезы"] = words_dict[russian]
            elif russian == "нужда":
                words_dict["нужде"] = words_dict[russian]
            elif russian == "вечный":
                words_dict["вечна"] = words_dict[russian]

        pattern = r'<b>([^(]+)\s*\(([^)]+)\)</b>'
        for german, russian in re.findall(pattern, scene.get("narrative", "")):
            hint = russian.strip()
            if hint not in words_dict:
                words_dict[hint] = german.strip()

        return words_dict

    @staticmethod
    def _initial_progress_percentage(phase_count):
        """Calculate initial progress for the progress bar."""
        if not phase_count:
            return 0
        return max(1, int(100 / phase_count))
