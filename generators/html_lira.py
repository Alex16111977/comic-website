"""HTML Generator for Lira Journey pages"""
import re

from .base import BaseGenerator
from .js_lira import LiraJSGenerator


class LiraHTMLGenerator(BaseGenerator):
    """Generate complete HTML pages in lira-journey style"""

    def generate_journey(self, character_file):
        """Generate journey page for a character"""
        character = self.load_character(character_file)
        journey_phases = character.get("journey_phases", [])
        js = LiraJSGenerator.generate(character)

        exercises = self._prepare_exercises(journey_phases)
        initial_description = journey_phases[0].get("description", "") if journey_phases else ""
        first_phase_title = journey_phases[0].get("title", "") if journey_phases else ""
        initial_progress = self._initial_progress_percentage(len(journey_phases))

        return self.render_template(
            "journey.html",
            character=character,
            journey_phases=journey_phases,
            exercises=exercises,
            initial_description=initial_description,
            initial_progress=initial_progress,
            first_phase_title=first_phase_title,
            js=js,
        )

    def _prepare_exercises(self, journey_phases):
        """Prepare exercises with blanks replaced by interactive spans."""
        exercises = []

        for index, phase in enumerate(journey_phases):
            scene = phase.get("theatrical_scene")
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
                    "phase_id": phase["id"],
                    "title": scene["title"],
                    "text": rendered_text,
                    "is_active": index == 0,
                }
            )

        return exercises

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
