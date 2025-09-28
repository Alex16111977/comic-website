#!/usr/bin/env python
"""
Тест генерації одного файлу з мнемотехнікою
"""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generators.html_lira import LiraHTMLGenerator
import config

# Генеруємо тестову сторінку
html_gen = LiraHTMLGenerator(config)
test_file = config.CHARACTERS_DIR / "king_lear.json"

if not test_file.exists():
    print("[ERROR] king_lear.json не знайдено!")
    sys.exit(1)

print("[START] Генерація тестової сторінки...")

# Генеруємо HTML
html = html_gen.generate_journey(test_file)

# КРИТИЧНІ ПЕРЕВІРКИ
checks = []

# 1. Перевірка CSS
has_css_vars = '--der-primary' in html and '--die-primary' in html and '--das-primary' in html
checks.append(('CSS змінні артиклів', has_css_vars))

# 2. Перевірка HTML структур
has_legend = 'articles-legend' in html
checks.append(('Легенда артиклів', has_legend))

has_vocab_grid = 'vocabulary-grid' in html
checks.append(('Сітка словника', has_vocab_grid))

has_quiz = 'articles-quiz' in html
checks.append(('Вправа на артиклі', has_quiz))

has_quiz_items = 'quiz-item' in html
checks.append(('Питання вправи', has_quiz_items))

has_vocab_cards = 'vocab-card' in html
checks.append(('Картки словника', has_vocab_cards))

# 3. Перевірка JavaScript
has_js_init = 'initArticlesQuiz' in html
checks.append(('JS ініціалізація', has_js_init))

# 4. Перевірка позиціонування (мнемотехніка після вправ)
exercises_pos = html.find('exercises-container') if 'exercises-container' in html else -1
# ВАЖЛИВО: шукаємо HTML елементи, а не CSS класи!
vocab_pos = html.find('<div class="vocabulary-grid">') if '<div class="vocabulary-grid">' in html else -1
quiz_pos = html.find('<section class="articles-quiz"') if '<section class="articles-quiz"' in html else -1
nav_pos = html.find('bottom-nav') if 'bottom-nav' in html else -1

# Мнемотехніка має бути між exercises та nav
correct_order = (exercises_pos > 0 and vocab_pos > exercises_pos and 
                nav_pos > vocab_pos and nav_pos > quiz_pos)
checks.append(('Правильний порядок секцій', correct_order))

# 5. Перевірка наявності style тегу в head
has_style_in_head = '<style>' in html and '</style>' in html and '</head>' in html
style_before_head_close = False
if has_style_in_head:
    style_pos = html.find('<style>')
    head_close_pos = html.find('</head>')
    style_before_head_close = style_pos < head_close_pos
checks.append(('CSS в head секції', style_before_head_close))

# Виводимо результати
print("=" * 60)
print("ТЕСТ ГЕНЕРАЦІЇ З МНЕМОТЕХНІКОЮ")
print("=" * 60)

success_count = 0
for name, status in checks:
    icon = "[OK]" if status else "[FAIL]"
    print(f"{icon} {name}: {status}")
    if status:
        success_count += 1

print("-" * 60)
print(f"Результат: {success_count}/{len(checks)} перевірок пройдено")

# Додаткова діагностика позицій
if not correct_order:
    print("\n[DEBUG] Позиції елементів:")
    print(f"  exercises-container: {exercises_pos}")
    print(f"  vocabulary-grid: {vocab_pos}")
    print(f"  articles-quiz: {quiz_pos}")
    print(f"  bottom-nav: {nav_pos}")

# Зберігаємо тестовий файл
test_output = Path(__file__).parent / "test_mnemo_integrated.html"
with open(test_output, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n[FILE] Тестовий файл збережено: {test_output.name}")
print("[TIP] Відкрийте файл в браузері для візуальної перевірки")

# Фінальний вердикт
if success_count == len(checks):
    print("\n[SUCCESS] Інтеграція працює!")
    sys.exit(0)
else:
    print("\n[ERROR] Інтеграція має проблеми!")
    sys.exit(1)
