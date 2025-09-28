#!/usr/bin/env python
"""
Точний аналіз позицій елементів
"""
from pathlib import Path

test_file = Path(__file__).parent / "test_mnemo_integrated.html"

if not test_file.exists():
    print("[ERROR] Тестовий файл не існує!")
    exit(1)

with open(test_file, 'r', encoding='utf-8') as f:
    html = f.read()

print("[ДЕТАЛЬНИЙ АНАЛІЗ]")
print("=" * 60)

# Шукаємо різні варіанти vocabulary-grid
searches = [
    ('.vocabulary-grid', "CSS клас"),
    ('<div class="vocabulary-grid">', "HTML елемент"),
    ('class="vocabulary-section"', "Vocabulary секція"), 
    ('articles-quiz', "Вправа на артиклі"),
    ('exercises-container', "Контейнер вправ"),
    ('bottom-nav', "Навігація")
]

for pattern, desc in searches:
    pos = html.find(pattern)
    if pos > 0:
        print(f"[{pos:6}] {desc}: {pattern}")
        # Показуємо контекст
        context_start = max(0, pos - 50)
        context_end = min(len(html), pos + 100)
        context = html[context_start:context_end]
        print(f"         Контекст: ...{repr(context)}...")
        print("-" * 60)

# Перевірка секції мнемотехніки
print("\n[ПОШУК] Шукаємо секцію мнемотехніки після exercises:")
exercises_pos = html.find('exercises-container')
if exercises_pos > 0:
    # Шукаємо vocabulary-section ПІСЛЯ exercises
    vocab_section_pos = html.find('class="vocabulary-section"', exercises_pos)
    if vocab_section_pos > 0:
        print(f"✅ Знайдено vocabulary-section після exercises на позиції {vocab_section_pos}")
        
        # Показуємо початок секції
        section_start = vocab_section_pos - 20
        section_end = vocab_section_pos + 200
        print("Початок секції:")
        print(html[section_start:section_end])
    else:
        print("❌ НЕ знайдено vocabulary-section після exercises")
        
        # Можливо вона вставлена інакше?
        legend_pos = html.find('articles-legend', exercises_pos)
        if legend_pos > 0:
            print(f"✅ Але знайдено articles-legend після exercises на позиції {legend_pos}")
