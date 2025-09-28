"""HTML Generator for Lira Journey pages."""
from __future__ import annotations

from pathlib import Path
from typing import Any
import re

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
        # mnemo_vocabulary генерується окремо для кожної позиції
        # mnemo_quiz генерується окремо для кожної позиції
        
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
        
        # НОВЕ: Вставка словника ЗВЕРХУ (після theatrical-scene, перед exercises)
        theatrical_end = html.find('</div><!-- end theatrical-scene -->')
        exercises_start = html.find('<div class="exercises-container">')
        
        if theatrical_end > 0 and exercises_start > theatrical_end:
            # Генеруємо словник для поточної фази
            first_phase_id = assets.phases[0].get('id') if assets.phases else None
            vocab_html = self.mnemo_gen.generate_vocabulary_section(character, phase_id=first_phase_id)
            
            # Вставляємо між театральною сценою та вправами
            insert_pos = theatrical_end + len('</div><!-- end theatrical-scene -->')
            html = html[:insert_pos] + f'\n\n        {vocab_html}\n\n' + html[insert_pos:]
            print(f"[DEBUG] Словник вставлено ЗВЕРХУ для {character['id']}")
        
        # Видаляємо існуючий порожній vocabulary-grid (якщо є)
        # Цей елемент знаходиться в оригінальному шаблоні і конфліктує з нашим
        if '<div class="vocabulary-grid"></div>' in html:
            html = html.replace('<div class="vocabulary-grid"></div>', '')
            print(f"[DEBUG] Видалено порожній vocabulary-grid для {character['id']}")
        
        # Аналогічно для всього vocabulary-section блоку
        vocab_pattern = r'<div class="vocabulary-section">\s*<h2>[^<]*</h2>\s*<div class="vocabulary-grid"></div>\s*[^<]*</div>'
        if re.search(vocab_pattern, html):
            html = re.sub(vocab_pattern, '', html)
            print(f"[DEBUG] Видалено порожню vocabulary-section для {character['id']}")
        
        # Вставляємо CSS мнемотехніки в head
        # Додаємо CSS стилі в head через style тег
        if mnemo_css and '</head>' in html:
            style_block = f'<style>\n{mnemo_css}\n</style>'
            html = html.replace('</head>', f'{style_block}\n</head>')
            print(f"[DEBUG] CSS мнемотехніки додано в head для {character['id']}")
        
        # ВИПРАВЛЕНО: Вставляємо вправу ВСЕРЕДИНУ exercises-container
        exercises_start = html.find('<div class="exercises-container">')
        if exercises_start > 0:
            # Знаходимо кінець exercises-container
            # Шукаємо закриваючий div для exercises-container
            exercises_end = html.find('</div><!-- end exercises-container -->')
            
            if exercises_end > exercises_start:
                # Генеруємо вправу для першої фази
                first_phase_id = assets.phases[0].get('id') if assets.phases else None
                mnemo_quiz = self.mnemo_gen.generate_articles_quiz(character, phase_id=first_phase_id)
                
                # Вставляємо вправу ВСЕРЕДИНУ exercises-container перед закриваючим тегом
                html = html[:exercises_end] + f'\n\n        {mnemo_quiz}\n\n        ' + html[exercises_end:]
                print(f"[DEBUG] Вправа вставлена ВСЕРЕДИНУ exercises для {character['id']}")
            else:
                # Якщо немає спеціального коментаря, шукаємо за структурою
                # Знаходимо всі закриваючі div після exercises-container
                search_pos = exercises_start + len('<div class="exercises-container">')
                
                # Рахуємо відкриті div теги
                div_count = 1
                pos = search_pos
                
                while div_count > 0 and pos < len(html):
                    next_open = html.find('<div', pos)
                    next_close = html.find('</div>', pos)
                    
                    if next_close == -1:
                        break
                    
                    if next_open != -1 and next_open < next_close:
                        div_count += 1
                        pos = next_open + 4
                    else:
                        div_count -= 1
                        if div_count == 0:
                            # Знайшли закриваючий div для exercises-container
                            first_phase_id = assets.phases[0].get('id') if assets.phases else None
                            mnemo_quiz = self.mnemo_gen.generate_articles_quiz(character, phase_id=first_phase_id)
                            
                            # Вставляємо перед закриваючим div
                            html = html[:next_close] + f'\n\n        {mnemo_quiz}\n\n        ' + html[next_close:]
                            print(f"[DEBUG] Вправа вставлена ВСЕРЕДИНУ exercises (альтернативний метод) для {character['id']}")
                            break
                        pos = next_close + 6
        else:
            print(f"[ERROR] exercises-container не знайдено для {character['id']}")
        
        return html
