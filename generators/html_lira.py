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
        
        # НОВЕ: Вставка словника ЗВЕРХУ (після блока theatrical-scenes, перед exercises)
        scenes_start = html.find('<div class="theatrical-scenes">')
        insert_pos = None

        if scenes_start != -1:
            search_pos = html.find('>', scenes_start)
            if search_pos != -1:
                pos = search_pos + 1
                div_count = 1

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
                            insert_pos = next_close + len('</div>')
                            break
                        pos = next_close + len('</div>')

        if insert_pos is not None:
            # Генеруємо словник для поточної фази
            first_phase_id = assets.phases[0].get('id') if assets.phases else None
            vocab_html = self.mnemo_gen.generate_vocabulary_section(character, phase_id=first_phase_id)

            # Вставляємо між театральною сценою та вправами
            html = html[:insert_pos] + f'\n\n        {vocab_html}\n\n' + html[insert_pos:]
            print(f"[DEBUG] Словник вставлено ЗВЕРХУ для {character['id']}")
        
        # Видаляємо placeholder-блок словника у вигляді <div class="vocabulary-section">...
        # Залишаємо недоторканим новий варіант, що використовує <section>.
        search_start = 0
        placeholder_removed = False

        while True:
            block_start = html.find('<div class="vocabulary-section">', search_start)
            if block_start == -1:
                break

            start_tag_end = html.find('>', block_start)
            if start_tag_end == -1:
                break

            pos = start_tag_end + 1
            depth = 1

            while depth > 0 and pos < len(html):
                next_open = html.find('<div', pos)
                next_close = html.find('</div>', pos)

                if next_close == -1:
                    break

                if next_open != -1 and next_open < next_close:
                    depth += 1
                    pos = next_open + 4
                else:
                    depth -= 1
                    pos = next_close + len('</div>')

            if depth != 0:
                # Не вдалося знайти коректне закриття блоку, припиняємо пошук.
                break

            block_end = pos
            block_content = html[block_start:block_end]

            if '<div class="vocabulary-grid"></div>' in block_content:
                html = html[:block_start] + html[block_end:]
                placeholder_removed = True
                search_start = block_start
            else:
                search_start = block_end

        if placeholder_removed:
            print(f"[DEBUG] Видалено placeholder vocabulary-section для {character['id']}")
        
        # Вставляємо CSS мнемотехніки в head
        # Додаємо CSS стилі в head через style тег
        if mnemo_css and '</head>' in html:
            style_block = f'<style>\n{mnemo_css}\n</style>'
            html = html.replace('</head>', f'{style_block}\n</head>')
            print(f"[DEBUG] CSS мнемотехніки додано в head для {character['id']}")
        
        # ВИПРАВЛЕНО: Вставляємо вправу ВСЕРЕДИНУ exercises-container
        exercises_start = html.find('<div class="exercises-container">')
        if exercises_start > 0:
            search_pos = html.find('>', exercises_start)

            if search_pos != -1:
                pos = search_pos + 1
                div_count = 1
                exercises_end = None

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
                            exercises_end = next_close
                            break
                        pos = next_close + len('</div>')

                if div_count == 0 and exercises_end is not None:
                    # Генеруємо вправу для першої фази
                    first_phase_id = assets.phases[0].get('id') if assets.phases else None
                    mnemo_quiz = self.mnemo_gen.generate_articles_quiz(character, phase_id=first_phase_id)

                    # Вставляємо вправу ВСЕРЕДИНУ exercises-container перед закриваючим тегом
                    html = html[:exercises_end] + f'\n\n        {mnemo_quiz}\n\n        ' + html[exercises_end:]
                    print(f"[DEBUG] Вправа вставлена ВСЕРЕДИНУ exercises для {character['id']}")
        else:
            print(f"[ERROR] exercises-container не знайдено для {character['id']}")
        
        return html
