#!/usr/bin/env python
"""
Патч для правильного розташування словника та вправи
"""
import sys
from pathlib import Path

html_file = Path(__file__).parent.parent / "generators" / "html_lira.py"

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Бекап
backup = html_file.with_suffix('.py.backup_mnemo')
with open(backup, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"[OK] Створено бекап: {backup.name}")

# ПАТЧ 1: Вимкнути стару вставку внизу
old_insert = '''        # Вставляємо HTML секції мнемотехніки між exercises та bottom-nav
        # Важливо: шукаємо патерн після exercises-container
        exercises_pos = html.find('exercises-container')
        if exercises_pos > 0:'''

new_insert = '''        # СТАРИЙ КОД ВИМКНЕНО - мнемотехніка тепер правильно розташована
        # Словник - зверху перед exercises
        # Вправа - всередині exercises  
        if False:  # Вимкнено'''

content = content.replace(old_insert, new_insert)

# ПАТЧ 2: Додати словник ПЕРЕД exercises-section
# Знаходимо рядок з vocabulary-section і замінюємо
old_vocab = '''        # Видаляємо існуючий порожній vocabulary-grid (якщо є)
        # Цей елемент знаходиться в оригінальному шаблоні і конфліктує з нашим
        if '<div class="vocabulary-grid"></div>' in html:
            html = html.replace('<div class="vocabulary-grid"></div>', '')
            print(f"[DEBUG] Видалено порожній vocabulary-grid для {character['id']}")'''

new_vocab = '''        # Вставляємо словник з мнемотехнікою в vocabulary-section
        # Замінюємо порожній vocabulary-grid на наш
        if '<div class="vocabulary-grid"></div>' in html:
            # Генеруємо картки слів з кольоровою кодировкою
            vocab_html = self.generate_vocabulary_cards(character)
            html = html.replace('<div class="vocabulary-grid"></div>', vocab_html)
            print(f"[DEBUG] Словник з мнемотехнікою додано для {character['id']}")'''

content = content.replace(old_vocab, new_vocab)

# ПАТЧ 3: Додати метод генерації карток словника
method_to_add = '''
    def generate_vocabulary_cards(self, character):
        """Генерує картки словника з кольоровою кодировкою для поточної фази"""
        html = '<div class="vocabulary-grid">'
        
        # Беремо першу фазу за замовчуванням (буде змінюватись через JS)
        first_phase = character.get('journey_phases', [{}])[0]
        vocab = first_phase.get('vocabulary', [])
        
        for word_data in vocab:
            german = word_data['german']
            article = self.mnemo_gen.extract_article(german)
            if article:
                word_only = german.replace(f"{article} ", "")
                color_class = f"is-{article}"
                color_data = self.mnemo_gen.GENDER_COLORS.get(article, {})
                
                html += f"""
                <div class="vocab-card {color_class}" data-article="{article}">
                    <div class="vocab-header">
                        <span class="article-chip {article}">
                            <span class="article-icon">{color_data.get('icon', '')}</span>
                            <span>{article}</span>
                        </span>
                        <div class="vocab-word">{word_only}</div>
                    </div>
                    <div class="vocab-translation">{word_data['russian']}</div>
                    <div class="vocab-transcription">{word_data['transcription']}</div>
                </div>"""
            
        html += '</div>'
        return html
'''

# Вставляємо новий метод після generate_journey
insert_pos = content.find('        return html')
if insert_pos > 0:
    content = content[:insert_pos] + '        return html' + method_to_add + '\n'
else:
    print("[ERROR] Не знайдено місце для вставки методу!")

# ПАТЧ 4: Додати вправу на артиклі в exercises-section
old_exercises = '''        # Отримуємо HTML і додаємо мнемотехніку
        html = self.template_engine.render(context)'''

new_exercises = '''        # Отримуємо HTML і додаємо мнемотехніку
        html = self.template_engine.render(context)
        
        # Додаємо вправу на артиклі в exercises-section
        if '</div>\n            </div>\n        </div>\n\n        <div class="exercises-container">' in html:
            # Генеруємо вправу для першої фази
            first_phase_id = assets.phases[0].get('id') if assets.phases else None
            articles_quiz = self.mnemo_gen.generate_articles_quiz(character, phase_id=first_phase_id)
            
            # Вставляємо перед exercises-container
            old_pattern = '</div>\n            </div>\n        </div>\n\n        <div class="exercises-container">'
            new_pattern = f"""</div>
            </div>
            
            <!-- Вправа на артиклі з мнемотехнікою -->
            {articles_quiz}
        </div>

        <div class="exercises-container">"""
            html = html.replace(old_pattern, new_pattern)
            print(f"[DEBUG] Вправа на артиклі додана в exercises для {character['id']}")'''

content = content.replace(old_exercises, new_exercises)

# Зберігаємо патч
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] html_lira.py пропатчено!")
print("Зміни:")
print("  1. Вимкнено стару вставку внизу")
print("  2. Словник тепер в vocabulary-section")
print("  3. Додано метод generate_vocabulary_cards")
print("  4. Вправа на артиклі в exercises-section")
