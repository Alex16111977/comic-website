"""HTML Generator for Lira Journey pages."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import BaseGenerator
from .mnemonics_gen import MnemonicsGenerator
from .html import (
    HeadGenerator,
    JourneyBuilder,
    JourneyTemplateEngine,
    TemplateContext,
    VocabularyProcessor,
)
from .js_lira import LiraJSGenerator


class LiraHTMLGenerator(BaseGenerator):
    """Generate complete HTML pages in Lira journey style."""

    def __init__(self, config: Any) -> None:
        super().__init__(config)
        self.vocabulary = VocabularyProcessor(self.config.DATA_DIR)
        self.journey_builder = JourneyBuilder(self.vocabulary)
        self.head_generator = HeadGenerator()
        self.template_engine = JourneyTemplateEngine(self)
        self.mnemo_gen = MnemonicsGenerator(config)

    def generate_journey(self, character_file: Path) -> str:
        character = self.load_character(character_file)
        self.vocabulary.enrich_character(character)
        assets = self.journey_builder.prepare(character)
        character["journey_phases"] = assets.phases
        progress = JourneyBuilder.initial_progress(assets.phases)
        head_context = self.head_generator.build(assets.phases, progress)
        js_bundle = LiraJSGenerator.generate(character)
        
        # Додаємо мнемотехніку
        mnemo_css = self.mnemo_gen.generate_css()
        mnemo_js = self.mnemo_gen.generate_javascript()
        mnemo_vocabulary = self.mnemo_gen.generate_vocabulary_section(character)
        mnemo_quiz = self.mnemo_gen.generate_articles_quiz(character)
        
        # Об'єднуємо JS
        js_bundle = js_bundle + "\n" + mnemo_js
        
        navigation = {
            "home_href": "../index.html",
            "home_label": "На главную",
            "home_icon": "←",
            "study_label": "СПИСОК ИЗУЧЕНИЯ",
        }
        context = TemplateContext(
            character=character,
            phases=assets.phases,
            exercises=assets.exercises,
            quizzes=assets.quizzes,
            quizzes_json=assets.quizzes_json,
            head=head_context,
            navigation=navigation,
            relations_metadata=assets.relations_metadata,
            js_bundle=js_bundle,
        )
        
        # Отримуємо HTML і додаємо мнемотехніку
        html = self.template_engine.render(context)
        
        # Вставляємо CSS мнемотехніки в head
        html = html.replace('</style>', mnemo_css + '\n</style>')
        
        # Додаємо секції мнемотехніки перед </main>
        html = html.replace('</main>', mnemo_vocabulary + mnemo_quiz + '</main>')
        
        return html
