#!/usr/bin/env python
"""
Виправлення синтаксичної помилки в html_lira.py
"""
import re
from pathlib import Path

html_file = Path(r'F:\AiKlientBank\KingLearComic\generators\html_lira.py')
backup_file = Path(r'F:\AiKlientBank\KingLearComic\generators\html_lira.py.backup_mnemo')

# Відновлюємо з бекапу
if backup_file.exists():
    with open(backup_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("[INFO] Відновлено з бекапу")
else:
    print("[ERROR] Бекап не знайдено!")
    exit(1)

# НОВИЙ ПАТЧ - правильний
# 1. Вимкнути стару вставку
old_pattern = r"exercises_pos = html\.find\('exercises-container'\)\s+if exercises_pos > 0:"
new_code = "# Стара вставка вимкнена\n        if False:  # exercises_pos > 0:"

content = re.sub(old_pattern, new_code, content, flags=re.MULTILINE)

# 2. Додати метод generate_vocabulary_cards ПІСЛЯ класу
method_code = '''
    def generate_vocabulary_cards(self, character):
        """Генерує картки словника з кольоровою кодировкою"""
        html = '<div class="vocabulary-grid">'
        
        # Беремо першу фазу 
        if character.get('journey_phases'):
            first_phase = character['journey_phases'][0]
            vocab = first_phase.get('vocabulary', [])
            
            for word_data in vocab:
                german = word_data.get('german', '')
                article = self.mnemo_gen.extract_article(german)
                if article:
                    word_only = german.replace(f"{article} ", "")
                    color_class = f"is-{article}"
                    color_data = self.mnemo_gen.GENDER_COLORS.get(article, {})
                    
                    html += f"""<div class="vocab-card {color_class}" data-article="{article}">
                        <div class="vocab-header">
                            <span class="article-chip {article}">
                                {article}
                            </span>
                            <div class="vocab-word">{word_only}</div>
                        </div>
                        <div class="vocab-translation">{word_data.get('russian', '')}</div>
                        <div class="vocab-transcription">{word_data.get('transcription', '')}</div>
                    </div>"""
            
        html += '</div>'
        return html
'''

# Вставляємо метод перед останнім return html
last_return_pos = content.rfind('        return html')
if last_return_pos > 0:
    content = content[:last_return_pos] + '        return html' + method_code + '\n'
    print("[OK] Метод generate_vocabulary_cards додано")

# 3. Оновити видалення vocabulary-grid
old_vocab_code = '''        if '<div class="vocabulary-grid"></div>' in html:
            html = html.replace('<div class="vocabulary-grid"></div>', '')
            print(f"[DEBUG] Видалено порожній vocabulary-grid для {character['id']}")'''

new_vocab_code = '''        if '<div class="vocabulary-grid"></div>' in html:
            vocab_html = self.generate_vocabulary_cards(character)
            html = html.replace('<div class="vocabulary-grid"></div>', vocab_html)
            print(f"[DEBUG] Словник з мнемотехнікою додано для {character['id']}")'''

content = content.replace(old_vocab_code, new_vocab_code)

# 4. Додати вправу на артиклі
# Знаходимо місце після рендерингу 
render_pos = content.find('html = self.template_engine.render(context)')
if render_pos > 0:
    # Вставляємо після рендера
    insert_pos = content.find('\n', render_pos) + 1
    
    quiz_code = '''
        # Додаємо вправу на артиклі  
        first_phase_id = assets.phases[0].get('id') if assets.phases else 'throne'
        articles_quiz_html = self.mnemo_gen.generate_articles_quiz(character, phase_id=first_phase_id)
        
        # Вставляємо в exercises-section
        exercises_marker = '<div class="exercises-section">'
        if exercises_marker in html:
            # Вставляємо після заголовка exercises
            pos = html.find('</h2>', html.find(exercises_marker)) + 5
            if pos > 5:
                html = html[:pos] + '\\n' + articles_quiz_html + html[pos:]
                print(f"[DEBUG] Вправа на артиклі додана для {character['id']}")
'''
    
    content = content[:insert_pos] + quiz_code + content[insert_pos:]
    print("[OK] Код вставки вправи додано")

# Зберігаємо виправлений файл
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("[SUCCESS] html_lira.py виправлено!")
