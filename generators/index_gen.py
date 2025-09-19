"""Index page generator with character cards"""
from .base import BaseGenerator


class IndexGenerator(BaseGenerator):
    """Generate index page with all character journeys"""

    def generate(self, character_files):
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

        return self.render_template(
            "index.html",
            cards=cards,
            character_count=len(cards),
            phase_total=phase_total,
            vocabulary_total=vocabulary_total,
        )
